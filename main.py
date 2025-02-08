import psutil
from time import sleep
from pymem import Pymem
from pymem.process import module_from_name

process_name = "cs2.exe"

def find_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

pid = find_pid_by_name(process_name)
if not pid:
    print(f"Process {process_name} not found!")
    exit()
else:
    print(f"Found PID of process {process_name}: {pid}")

try:
    pm = Pymem(pid)
    print(f"Connected to process: {process_name} (PID: {pid})")
except Exception as e:
    print(f"Error connect to: {e}")
    exit()

module_name = "client.dll"
base_offset = 0x018AFE08
pointer_offset = 0x54

try:
    module = module_from_name(pm.process_handle, module_name)
    base_address = module.lpBaseOfDll
    print(f"Base address of {module_name}: {hex(base_address)}")
except Exception as e:
    print(f"Error getting address: {e}")
    exit()

pointer_address = base_address + base_offset
print(f"Pointer address: {hex(pointer_address)}")

try:
    dynamic_address = pm.read_longlong(pointer_address)
    print(f"Dynamic address (pointer): {hex(dynamic_address)}")
except Exception as e:
    print(f"Error with reading: {e}")
    exit()

final_address = dynamic_address + pointer_offset
print(f"Final address: {hex(final_address)}")

try:
    current_value = pm.read_int(final_address)  # Читаем 4 байта (int)
    print(f"Current value at address {hex(final_address)}: {current_value}")
except Exception as e:
    print(f"Error with reading: {e}")
    exit()

try:
    new_value = int(input("\nEnter a new rating in Premier (integer): "))
    pm.write_int(final_address, new_value)
    print(f"New value {new_value} written to address {hex(final_address)}")
    sleep(3)
except Exception as e:
    print(f"Error with writing: {e}")
