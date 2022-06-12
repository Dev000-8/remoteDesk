# KOKDesk Server Program

Self-host your own KOKDesk server, it is free and open source.

```bash
cargo build --release
```

Two executables will be generated in target/release.
  - hbbs - KOKDesk ID/Rendezvous server
  - hbbr - KOKDesk relay server


## docker-compose

If you have Docker and would like to use it, an included `docker-compose.yml` file is included. Edit line 16 to point to your relay server (the one listening on port 21117). You can also edit the volume lines (L18 and L33) if you need.

