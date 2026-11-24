# æ TV

`æ TV` is the governed evolution of a media player for the Internet of Agents.

VLC answers: **“Can this file play?”**  
æ TV answers: **“Who authorized this channel, which voice speaks, what did the agent do, and where is the receipt?”**

```text
HUMAN://ROOT → æ policy → ae router → channel → playback/voice → RECEIPT
```

## Definition

æ TV is a channel-based projection surface where:

- a **channel** is an address, not a file path;
- a **program** is a receipted artifact, not a passive stream;
- a **voice** is a bound identity, not a soundtrack;
- an **agent** may curate, narrate, and play, but may not sign;
- every play, pause, seek, and voice binding leaves a receipt.

## Channel ontology

| Channel | Address | Content | Voice |
|---|---|---|---|
| `origin` | `æ://origin` | implementation atlas and proof | `M2` |
| `sovereign` | `æ://sovereign` | namespace film and law | `SOVÆREIGN` |
| `tinyVOICE` | `æ://tiny-voice` | voice demos and lessons | `F2`, `M2` |
| `asimov` | `æ://asimov` | robot body, twin, face states | `ROBOT` |
| `dao` | `æ://dao` | governance and native head viewport | `M2` |
| `course` | `æ://course` | OSW lessons | `F2`, `M2` |
| `gallery` | `æ://gallery` | published artifacts | bound per artifact |

## Harness mapping

| VLC concept | æ TV replacement |
|---|---|
| playlist | governed channel queue |
| media item | receipt-bound artifact |
| codec/container | transport detail under `ffmpeg` harness |
| playback control | `ae` op routed to `control` / `vlc` harness |
| subtitles | tinyTELEPROMPTER line band |
| voice track | tinyVOICE identity binding |
| media library | channel registry with hashes and receipts |
| remote control | `HUMAN://ROOT` approval gate |

## Build an episode

```text
ae({
  op:"tv_episode",
  channel:"æ://tiny-voice",
  format:"916",
  voice:"M2",
  lines:[
    {text:"Human root to æ to receipt.", voice:"F2"},
    {text:"The channel is an address, not a file path.", voice:"M2"}
  ],
  out:"/opt/data/cache/scratch/ae-tv-episode.mp4"
})
```

The op writes `TTS://SPEAK`, `FFMPEG://RENDER`, `FFMPEG://PROBE`, and
`VIDEO://QC` records through the unified `ae` receipt chain.

## Governance

æ TV fails closed:

1. No channel without an address.
2. No artifact without a hash.
3. No playback without a receipt.
4. No voice clone without `VOICE://BIND`.
5. No agent-curated channel without `HUMAN://ROOT` approval.
6. No claim that playback is authority. Playback is a projection; authority stays human.

## Why this is the natural evolution

VLC was built for a world of local files. æ TV is built for a world of agents, addresses, identity bindings, and public receipts.

The one-person company movement needs a screen that can hold many governed agents without losing the human root. æ TV is that screen.

`HUMAN://ROOT → æ → RECEIPT`

#opensourceware #internetofagents
