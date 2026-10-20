# Architecture

```
               ┌────────────────────┐
               │  __main__.py       │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │ bootstrap/runtime  │  attach, tick loop, detach
               └─────────┬──────────┘
        ┌────────────────┼─────────────────┐
        │                │                 │
  ┌─────▼─────┐   ┌──────▼──────┐   ┌──────▼──────┐
  │  core/    │   │  handlers/  │   │  services/  │
  │ attacher  │   │  godmode    │   │  entity_    │
  │ memory    │   │  aimbot     │   │  scanner    │
  │ offsets   │   │  esp        │   └─────────────┘
  └───────────┘   │  infinite_  │
                  │  ammo       │
                  └─────────────┘
```

Handlers are ticked at `runtime.tick_ms` (default 50 ms). Each handler is
responsible for reading its own offsets and swallowing `OSError` — a dead
`ReadProcessMemory` should never take the trainer down.