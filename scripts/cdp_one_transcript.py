#!/usr/bin/env python3
"""Fetch one YouTube transcript via a live Chrome CDP session (port 9222)."""

from __future__ import annotations

import json
import sys
import time
import urllib.request

import websocket  # type: ignore

CDP = "http://127.0.0.1:9222"
VID = sys.argv[1] if len(sys.argv) > 1 else "MI4B18okOyY"


def http_json(url: str):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read().decode())


def page_ws() -> str:
    targets = http_json(f"{CDP}/json")
    for t in targets:
        if t.get("type") == "page" and not t.get("url", "").startswith("chrome-extension"):
            return t["webSocketDebuggerUrl"]
    # open a new tab
    t = http_json(f"{CDP}/json/new?about:blank")
    return t["webSocketDebuggerUrl"]


class Cdp:
    def __init__(self, url: str):
        self.ws = websocket.create_connection(url, timeout=30)
        self.n = 0

    def call(self, method: str, **params):
        self.n += 1
        mid = self.n
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result") or {}

    def eval(self, expr: str, await_p=True):
        res = self.call(
            "Runtime.evaluate",
            expression=expr,
            returnByValue=True,
            awaitPromise=await_p,
        )
        if res.get("exceptionDetails"):
            raise RuntimeError(res["exceptionDetails"])
        return (res.get("result") or {}).get("value")


def extract_js() -> str:
    return r"""
(async () => {
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  const readPlayer = () => {
    const p = window.ytInitialPlayerResponse
      || window.ytplayer?.config?.args?.raw_player_response
      || null;
    return p;
  };
  let player = readPlayer();
  for (let i = 0; i < 20 && !player; i++) {
    await sleep(500);
    player = readPlayer();
  }
  if (!player) {
    // try from script tags
    const html = document.documentElement.innerHTML;
    const m = html.match(/ytInitialPlayerResponse\s*=\s*(\{.+?\});/s);
    if (m) { try { player = JSON.parse(m[1]); } catch(e) {} }
  }
  const title = player?.videoDetails?.title || document.title || '';
  const author = player?.videoDetails?.author || '';
  const length = Number(player?.videoDetails?.lengthSeconds || 0);
  const tracks = player?.captions?.playerCaptionsTracklistRenderer?.captionTracks || [];
  const play = player?.playabilityStatus || {};
  if (!tracks.length) {
    return {ok:false, title, author, length, play, reason:'no_caption_tracks', ntracks:0};
  }
  const prefer = tracks.find(t => (t.languageCode||'').startsWith('pt')) || tracks[0];
  let url = prefer.baseUrl || '';
  if (url && !url.includes('fmt=')) url += '&fmt=json3';
  const resp = await fetch(url, {credentials:'include'});
  const text = await resp.text();
  return {
    ok: resp.ok && text.length > 20,
    title, author, length,
    lang: prefer.languageCode,
    kind: prefer.kind || '',
    status: resp.status,
    bytes: text.length,
    body: text.slice(0, 250000),
    ntracks: tracks.length,
    playStatus: play.status || null,
  };
})()
"""


def parse_json3(body: str) -> list[dict]:
    data = json.loads(body)
    out = []
    for ev in data.get("events") or []:
        segs = ev.get("segs") or []
        text = "".join(s.get("utf8") or "" for s in segs).strip()
        if not text or text == "\n":
            continue
        out.append({"start": (ev.get("tStartMs") or 0) / 1000.0, "text": " ".join(text.split())})
    return out


def main() -> int:
    ws = page_ws()
    cdp = Cdp(ws)
    cdp.call("Page.enable")
    cdp.call("Runtime.enable")
    url = f"https://www.youtube.com/watch?v={VID}&hl=pt"
    cdp.call("Page.navigate", url=url)
    # wait load
    time.sleep(6)
    result = cdp.eval(extract_js())
    if not isinstance(result, dict):
        print(json.dumps({"ok": False, "error": "no_js_result", "raw": str(result)[:300]}))
        return 1
    if not result.get("ok"):
        print(json.dumps({k: result.get(k) for k in result if k != "body"}, ensure_ascii=False))
        return 2
    segs = []
    body = result.get("body") or ""
    if body.lstrip().startswith("{"):
        segs = parse_json3(body)
    print(json.dumps({
        "ok": True,
        "video_id": VID,
        "title": result.get("title"),
        "author": result.get("author"),
        "length": result.get("length"),
        "lang": result.get("lang"),
        "kind": result.get("kind"),
        "segments": len(segs),
        "preview": segs[:4],
    }, ensure_ascii=False))
    out = f"/tmp/yt-caps/{VID}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"meta": result, "segments": segs}, f, ensure_ascii=False)
    print("WROTE", out)
    return 0 if segs else 3


if __name__ == "__main__":
    raise SystemExit(main())
