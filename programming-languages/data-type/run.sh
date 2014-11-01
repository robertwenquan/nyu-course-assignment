gcc -m64 -o type.m64 type.c
gcc -m32 -o type.m32 type.c

echo "Type length for (x86_64):"
./type.m64

echo "Type length for (IA32):"
./type.m32

