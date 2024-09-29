import sys
import os

package_name_list = ['scipy']
package_names = ' '.join(package_name_list)

print(f'Install packages: {package_names}')

python_path = sys.executable
print(f'python_path: {python_path}')

cmd = f'{python_path} -m pip install {package_names}'
print(f'Run cmd: `{cmd}`')
os.system(cmd)