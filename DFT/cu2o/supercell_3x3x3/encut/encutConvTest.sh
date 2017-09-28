#!/bin/bash
for i in {300..800..50};
 do 
  mkdir ENCUT$i
  cd ENCUT$i
  cp ../INCAR .
  cp ../POSCAR .
  cp ../jobfile . 
  sed -i 7s/250/$i/ INCAR
  makepot . O
  makekpoints
  cd ..
 done
