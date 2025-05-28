#!/bin/bash
set -e

echo "Mise à jour des paquets..."
sudo apt-get update

echo "Installation des dépendances système..."
sudo apt-get install -y \
  build-essential cmake git \
  libusb-1.0-0-dev \
  python3-dev python3-pip \
  python3-numpy python3-opencv python3-pygame \
  libfreenect-dev

echo "Compilation et installation de libfreenect (bindings Python)..."
cd $HOME
if [ ! -d libfreenect ]; then
  git clone https://github.com/OpenKinect/libfreenect.git
fi
cd libfreenect
mkdir -p build && cd build
cmake .. 
make -j4
sudo make install
sudo ldconfig

echo "Installation des bindings Python de libfreenect..."
cd ../bindings/python
sudo python3 setup.py install

echo "Installation terminée."
