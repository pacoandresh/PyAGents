packages_python="/usr/local/lib/python3.8/dist-packages"
packages_local=$HOME/.local/lib/python3.8/site-packages
dir_PyAgent=$PWD/PyAgent
dir_DAR_cli=$PWD/DAR_cli
dir_DARPy=$PWD/DARPy
echo creando enlace: $dir_PyAgent en $packages_python
sudo rm -f $packages_python/PyAgent
sudo ln -s  $dir_PyAgent $packages_python/PyAgent
sudo ln -s $dir_PyAgent $packages_local/PyAgent

echo creando enlace: $dir_DARPy en $packages_python
sudo rm -f $packages_python/DARPy
sudo ln -s  $dir_DARPy $packages_python/DARPy
sudo ln -s  $dir_DARPy $packages_local/DARPy

echo creando enlace: $dir_DAR_cli en $packages_python
sudo rm -f $packages_python/DAR_cli
sudo ln -s  $dir_DAR_cli $packages_python/DAR_cli
sudo ln -s  $dir_DAR_cli $packages_local/DAR_cli

echo $DARPy
export AGENTS=$PWD/Agents
echo insert this line in your .bashrc
echo export AGENTS=$PWD/Agents

