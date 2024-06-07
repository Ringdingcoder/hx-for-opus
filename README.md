# Winword 1 (Opus) build without excessive amounts of conventional memory

See http://www.computerhistory.org/atchm/microsoft-word-for-windows-1-1a-source-code/

It has always irked me that the supplied OS/2-hosted compiler was not accessible from DOS. After all, all more modern DOS compilers used DOS extenders to have access to somewhat more reasonable amounts of memory. The HX DOS extender should in theory enable this, but there are some stumbling blocks.

First, the executables must be stubbed with the DPMI loader, and the OS type must be set to OS/2.

Second, there are some bugs/oversights in the NE loader and OS/2 emulation libraries regarding command line handling.

With everything in place and with the fixed argument handling, a successful build is just a makeopus invocation away. For me, it succeeds with as little as 325 KB of available DOS memory. Tested under real DOS 6.22, also WfW 3.11 as well as Windows XP. All of them running in VirtualBox. Also tested on qemu.

- The patched HX files are pre-built under `bin/` in this repository, so you might skip the next two steps.
- Unzip `HXRT217.zip`, `HXSRC217.zip`, `HXDEV217.zip`, `HXD16217.zip`.
- Patch `SRC/DOSXXX/DOSEXEC.ASM` and `SRC/DPMILDR/DPMILDR.ASM` according to this repo. Build the `DOSXXX` and `DPMILDR` directories (at least `DOSCALLS.DLL` and `DPMILD16.EXE`).
- Take `CSL.EXE` and `CSL2.EXE` from `Opus/tools/os2` and apply `DPMIST16.BIN` using `renestub.py`.
- For operation under Windows (NTVDM): Patch 0xffff to 0x0000 at offsets 0x1ec9f (`CSL.EXE`) / 0x133c7 (`CSL2.EXE`). These are invalid seeks to file position -1.
- Copy `DOSCALLS.DLL`, `DPMILD16.EXE`, `CSL.EXE`, `CSL2.EXE` into `Opus/tools/dos`.
- Also stub `MASM.EXE` from `Opus/tools` and replace it with the stubbed version.
- Run `tools\makeopus` normally.

Initially, this repo hosted the resulting CSL* binaries, but the Winword museum license does not permit this, so I had to remove them.

Also, at the time I originally did this project, I was not aware of the Microsoft Family API and thus missed the fact that the DOS version of MASM 5 is a bound executable, and thus the same file is already both the DOS and the OS/2 version.

Additionally, I became aware that it does not work on any NT before Windows XP; ironically, this happens to be the case because these versions support OS/2 executables natively, and im2obj.exe does not seem to work in this mode. I could determine that it issues a large DosRead operation into a not-so-large buffer, and the Windows OS/2 subsystem probes the last byte of the buffer to make sure that it is writable, thus crashing it. The data read from file is apparently never large enough to overflow the buffer; it is specifially the probe that crashes it.
