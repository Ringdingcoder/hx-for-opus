# Winword 1 (Opus) build in 520K memory

See http://www.computerhistory.org/atchm/microsoft-word-for-windows-1-1a-source-code/

It has always irked me that the supplied OS/2-hosted compiler was not accessible from DOS. After all, all more modern DOS compilers used DOS extenders to have access to somewhat more reasonable amounts of memory. The HX DOS extender should in theory enable this, but there are some stumbling blocks.

First, the DPMI loader stub must be fixed onto the executables, and the OS type must be set to OS/2.

Second, there are some bugs/oversights in the NE loader and OS/2 emulation libraries regarding command line handling.

With everything in place and with the fixed argument handling, a successful build is just a makeopus invocation away. The most memory-hungry job during the entire process is MASM, of which there is no OS/2 version in the distribution, so there is not that much leeway, but 520K of free conventional memory is something that's trivially easy to reach in every setting.

Tested under real DOS 6.22, also WfW 3.11 as well as Windows XP. All of them running in VirtualBox.

- The patched HX files are pre-built under bin/ in this repository, so you might skip the next two steps.
- Unzip HXRT217.zip, HXSRC217.zip, HXDEV217.zip, HXD16217.zip.
- Patch SRC/DOSXXX/DOSEXEC.ASM and SRC/DPMILDR/DPMILDR.ASM according to this repo. Build the DOSXXX and DPMILDR directories (at least DOSCALLS.DLL and DPMILD16.EXE).
- Take CSL.EXE and CSL2.EXE from Opus/tools/os2 and apply DPMIST16.BIN using renewstub.py.
- For operation under Windows (NTVDM): Patch 0xffff to 0x0000 at offsets 0x1ec9f (CSL.EXE) / 0x133c7 (CSL2.EXE). These are invalid seeks to file position -1.
- Copy DOSCALLS.DLL, DPMILD16.EXE, CSL.EXE, CSL2.EXE into Opus/tools/dos.
- Run tools\makeopus normally.
