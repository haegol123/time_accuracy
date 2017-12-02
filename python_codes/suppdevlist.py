#-*- coding: utf-8 -*-
#------------------------------------------------------------
# filename: suppdevlist.py

# written by Jaewook Kang @ July 2017
#------------------------------------------------------------
from pandas import DataFrame

#
# ANDROID = \
# ['IM-100K','IM-100S','IM-100L',\
#  'IM-A890K','IM-A890S','IM-A890L',\
#  'IM-A910K','IM-A910S','IM-A910L',\
#  'LG-F320K','LG-F320L','LG-F320S',\
#  'LG-F350K','LG-F350S','LG-F350L',\
#  'LG-F400K','LG-F400L','LG-F400S',\
#  'LG-F410K','LG-F410S','LG-F410L',\
#  'LG-F460K','LG-F460L','LG-F460S',\
#  'LG-F490K','LG-F490S','LG-F490L',\
#  'LG-F500K','LG-F500L','LG-F500S',\
#  'LG-F510K',\
#  'LG-F520K',\
#  'LG-F560K',\
#  'LG-F600K','LG-F600L','LG-F600S',\
#  'LG-F620K',\
#  'LG-F650K',\
#  'LG-F670K',\
#  'LG-F700K','LG-F700L','LG-F700S',\
#  'LG-F720K',\
#  'LG-F750K',\
#  'LG-F800K', 'LG-F800L','LG-F800S',\
#  'LG-F820L',\
#  'LGM-G600K','LGM-G600L','LGM-G600S',\
#  'LGM-K121K',\
#  'LGM-X320K',\
#  'Nexus 5X',\
#  'SHV-E210K',\
#  'SHV-E250K','SHV-E250L','SHV-E250S',\
#  'SHV-E300K',\
#  'SHV-E310K',\
#  'SHV-E330K','SHV-E330S',\
#  'SM-A310N0',\
#  'SM-A500K',\
#  'SM-A510K',\
#  'SM-A520K','SM-A520L','SM-A520S',\
#  'SM-A700K',\
#  'SM-A710K','SM-A710L','SM-A710S',\
#  'SM-A800S',\
#  'SM-A810S',\
#  'SM-G600S',\
#  'SM-G610K', 'SM-G610S','SM-G610L',\
#  'SM-G710K',\
#  'SM-G720N0',\
#  'SM-G850K',\
#  'SM-G900K','SM-G900S','SM-G900L',\
#  'SM-G906K','SM-G906L','SM-G906S',\
#  'SM-G920K','SM-G920L','SM-G920S',\
#  'SM-G925K','SM-G925L','SM-G925S',\
#  'SM-G928K','SM-G928S','SM-G928L',\
#  'SM-G930K','SM-G930L','SM-G930S',\
#  'SM-G935K','SM-G935L','SM-G935S',\
#  'SM-G950N',\
#  'SM-G955N',\
#  'SM-J500N0',\
#  'SM-J510K','SM-J510L','SM-J510S',\
#  'SM-J530K',\
#  'SM-J700K',\
#  'SM-J710K',\
#  'SM-N750K',\
#  'SM-N900K','SM-N900L','SM-N900S',\
#  'SM-N910K','SM-N910L','SM-N910S',\
#  'SM-N915K','SM-N915S','SM-N915L',\
#  'SM-N916K','SM-N916L','SM-N916S',\
#  'SM-N920K','SM-N920L','SM-N920S',\
#  'SM-N935K','SM-N935S','SM-N935L',\
#  'TG-L800S','TG-L900S']


ANDROID = \
[\
 ['IM-100K','im100'],\
 ['IM-100S','im100'],\
 ['IM-100L','im100'],\
 ['IM-A890K','vegasecretnote'],\
 ['IM-A890S','vegasecretnote'],\
 ['IM-A890L','vegasecretnote'],\
 ['IM-A910K','vegairon2'],\
 ['IM-A910S','vegairon2'],\
 ['IM-A910L','vegairon2'],\
 ['LG-F320K','g2'],\
 ['LG-F320L','g2'],\
 ['LG-F320S','g2'],\
 ['LG-F350K','gpro2'],\
 ['LG-F350S','gpro2'],\
 ['LG-F350L','gpro2'],\
 ['LG-F400K','g3'],\
 ['LG-F400L','g3'],\
 ['LG-F400S','g3'],\
 ['LG-F410K','g3'],\
 ['LG-F410S','g3'],\
 ['LG-F410L','g3'],\
 ['LG-F460K','g3'],\
 ['LG-F460L','g3'],\
 ['LG-F460S','g3'],\
 ['LG-F490K','g3'],\
 ['LG-F490S','g3'],\
 ['LG-F490L','g3'],\
 ['LG-F500K','g4'],\
 ['LG-F500L','g4'],\
 ['LG-F500S','g4'],\
 ['LG-F510K','gflex2'],\
 ['LG-F520K','aka'],\
 ['LG-F560K','gstylo'],\
 ['LG-F600K','v10'],\
 ['LG-F600L','v10'],\
 ['LG-F600S','v10'],\
 ['LG-F620K','class'],\
 ['LG-F650K','xscreen'],\
 ['LG-F670K','k10'],\
 ['LG-F700K','g5'],\
 ['LG-F700L','g5'],\
 ['LG-F700S','g5'],\
 ['LG-F720K','gstylo2'],\
 ['LG-F750K','xpower'],\
 ['LG-F800K','v20'],\
 ['LG-F800L','v20'],\
 ['LG-F800S','v20'],\
 ['LG-F820L','f820'],\
 ['LGM-G600K','g6'],\
 ['LGM-G600L','g6'],\
 ['LGM-G600S','g6'],\
 ['LGM-K121K','x400'],\
 ['LGM-X320K','x500'],\
 ['Nexus 5X','nex5x'],\
 ['SHV-E210K','s3'],\
 ['SHV-E250K','note2'],\
 ['SHV-E250L','note2'],\
 ['SHV-E250S','note2'],\
 ['SHV-E300K','s4'],\
 ['SHV-E310K','mega'],\
 ['SHV-E330K','s4lte'],\
 ['SHV-E330S','s4lte'],\
 ['SM-A310N0','a3v16'],\
 ['SM-A500K','a5'], \
 ['SM-A500S', 'a5'], \
 ['SM-A500L', 'a5'], \
 ['SM-A510K','a5v16'], \
 ['SM-A510L','a5v16'],
 ['SM-A510S','a5v16'], \
 ['SM-A520K','a5v17'],\
 ['SM-A520L','a5v17'],\
 ['SM-A520S','a5v17'],\
 ['SM-A700K','a7'], \
 ['SM-A700L', 'a7'], \
 ['SM-A700S', 'a7'], \
 ['SM-A710K','a7v16'],\
 ['SM-A710L','a7v16'],\
 ['SM-A710S','a7v16'], \
 ['SM-A720K', 'a7v17'], \
 ['SM-A720L', 'a7v17'], \
 ['SM-A720S', 'a7v17'], \
 ['SM-A800S','a8'],\
 ['SM-A810S','a8v16'],\
 ['SM-G600S','on7'],\
 ['SM-G610K','j7p'],\
 ['SM-G610S','j7p'],\
 ['SM-G610L','j7p'],\
 ['SM-G710K','grand2'],\
 ['SM-G720N0','grandmax'],\
 ['SM-G850K','alpha'],\
 ['SM-G900K','s5'],\
 ['SM-G900S','s5'],\
 ['SM-G900L','s5'],\
 ['SM-G906K','s5lte'],\
 ['SM-G906L','s5lte'],\
 ['SM-G906S','s5lte'],\
 ['SM-G920K','s6'],\
 ['SM-G920L','s6'],\
 ['SM-G920S','s6'],\
 ['SM-G925K','s6edge'],\
 ['SM-G925L','s6edge'],\
 ['SM-G925S','s6edge'],\
 ['SM-G928K','s6edgep'],\
 ['SM-G928S','s6edgep'],\
 ['SM-G928L','s6edgep'],\
 ['SM-G930K','s7'],\
 ['SM-G930L','s7'],\
 ['SM-G930S','s7'],\
 ['SM-G935K','s7edge'],\
 ['SM-G935L','s7edge'],\
 ['SM-G935S','s7edge'],\
 ['SM-G950N','s8'],\
 ['SM-G955N','s8p'],\
 ['SM-J500N0','j5'],\
 ['SM-J510K','j5v16'],\
 ['SM-J510L','j5v16'],\
 ['SM-J510S','j5v16'],\
 ['SM-J530K','j5v17'], \
 ['SM-J530L','j5v17'], \
 ['SM-J530S','j5v17'], \
 ['SM-J700K','j7'],\
 ['SM-J710K','j7v16'], \
 ['SM-J730K', 'j7v17'], \
 ['SM-J730L', 'j7v17'],
 ['SM-J730S', 'j7v17'], \
 ['SM-N750K','note3'],\
 ['SM-N900K','note3'],\
 ['SM-N900L','note3'],\
 ['SM-N900S','note3'],\
 ['SM-N910K','note4'],\
 ['SM-N910L','note4'],\
 ['SM-N910S','note4'],\
 ['SM-N915K','noteedge'],\
 ['SM-N915S','noteedge'],\
 ['SM-N915L','noteedge'],\
 ['SM-N916K','note4lte'],\
 ['SM-N916L','note4lte'],\
 ['SM-N916S','note4lte'],\
 ['SM-N920K','note5'],\
 ['SM-N920L','note5'],\
 ['SM-N920S','note5'],\
 ['SM-N935K','notefe'],\
 ['SM-N935S','notefe'],\
 ['SM-N935L','notefe'],\
 ['SM-N950N','note8'], \
 ['SM-N950K', 'note8'], \
 ['SM-N950S', 'note8'], \
 ['SM-N950L', 'note8'], \
 ['TG-L800S','luna'],\
 ['TG-L900S','luna2']\
  ]


dfANDROID = DataFrame(data=ANDROID,columns=['phoneModel','devicename'])