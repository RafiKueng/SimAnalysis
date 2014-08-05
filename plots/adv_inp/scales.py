# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 00:25:22 2014

@author: RafiK
"""

scales = {}
scales['ASW000102p'] = {}
scales['ASW000102p'][6941] = {
#    Map radius           = 0.1851 [arcsec] Distance to center of outer pixel.
#    Map Extent           = 0.1929 [arcsec] Distance to outer edge of outer pixel.
#    top_level_cell_size  = 0.0154 [arcsec]
#    Map radius           = 1.1168 [kpc]    H0inv=13.7
#    Map Extent           = 1.1633 [kpc]    H0inv=13.7
    'map_r'           : {'arcsec':0.1851, 'kpc': 1.1168},
    'map_e'           : {'arcsec':0.1929, 'kpc': 1.1633},
}
  
scales['ASW000195x'] = {}
scales['ASW000195x'][6975] = {
    # Pixel radius         = 12
    # Map radius           = 0.4118 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.4290 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0343 [arcsec]
    # Map radius           = 2.1836 [kpc]    H0inv=13.7
    # Map Extent           = 2.2746 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1820 [kpc]    H0inv=13.7
    'map_r'           : {'arcsec':0.4118, 'kpc': 2.1836},
    'map_e'           : {'arcsec':0.4290, 'kpc': 2.2746},
}


scales['ASW0001hpf'] = {}
scales['ASW0001hpf'][6915] = {
    # Map radius           = 0.1213 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1264 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0101 [arcsec]
    # Map radius           = 0.7318 [kpc]    H0inv=13.7
    # Map Extent           = 0.7623 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.1213, 'kpc': 0.7318},
    'map_e'           : {'arcsec':0.1264, 'kpc': 0.7623},
}

scales['ASW0002z6f'] = {}
scales['ASW0002z6f'][6919] = {
    # Map radius           = 0.3153 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.3284 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0263 [arcsec]
    # Map radius           = 1.9018 [kpc]    H0inv=13.7
    # Map Extent           = 1.9810 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.3153, 'kpc':1.9018 },
    'map_e'           : {'arcsec':0.3284, 'kpc':1.9810 },
}

scales['ASW0000vqg'] = {}
scales['ASW0000vqg'][6937] = {
    # Map radius           = 0.2163 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2253 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0180 [arcsec]
    # Map radius           = 0.7024 [kpc]    H0inv=13.7
    # Map Extent           = 0.7316 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.2163, 'kpc':0.7024 },
    'map_e'           : {'arcsec':0.2253, 'kpc':0.7316 },
}

scales['ASW000102p'] = {}
scales['ASW000102p'][6941] = {
    # Map radius           = 0.1851 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1929 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0154 [arcsec]
    # Map radius           = 1.1168 [kpc]    H0inv=13.7
    # Map Extent           = 1.1633 [kpc]    H0inv=13.7

    'map_r'           : {'arcsec':0.1851, 'kpc':1.1168 },
    'map_e'           : {'arcsec':0.1929, 'kpc':1.1633 },
}

scales['ASW000195x'] = {}
scales['ASW000195x'][6975] = {
    # Pixel radius         = 12
    # Map radius           = 0.4118 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.4290 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0343 [arcsec]
    # Map radius           = 2.1836 [kpc]    H0inv=13.7
    # Map Extent           = 2.2746 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1820 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.4118, 'kpc':2.1836 },
    'map_e'           : {'arcsec':0.4290, 'kpc':2.2746 },
}

scales['ASW0004oux'] = {}
scales['ASW0004oux'][6990] = {
    # Pixel radius         = 12
    # Map radius           = 0.2618 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2727 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0218 [arcsec]
    # Map radius           = 1.5794 [kpc]    H0inv=13.7
    # Map Extent           = 1.6452 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1316 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.2618, 'kpc':1.5794 },
    'map_e'           : {'arcsec':0.2727, 'kpc':1.6452 },
}


scales['ASW0000h2m'] = {}
'''
scales['ASW0000h2m'][7020] = {
    # Pixel radius         = 12
    # Map radius           = 0.1868 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1946 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0156 [arcsec]
    # Map radius           = 1.1266 [kpc]    H0inv=13.7
    # Map Extent           = 1.1735 [kpc]    H0inv=13.7
    # top_level_cell       = 0.0939 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0
    
    'map_r'           : {'arcsec':0.1868, 'kpc':1.1266 },
    'map_e'           : {'arcsec':0.1946, 'kpc':1.1735 },
}
'''
'''
scales['ASW0000h2m'][7021] = {
    # Pixel radius         = 12
    # Map radius           = 0.1993 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2076 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0166 [arcsec]
    # Map radius           = 1.2022 [kpc]    H0inv=13.7
    # Map Extent           = 1.2523 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1002 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    'map_r'           : {'arcsec':0.1993, 'kpc':1.2022 },
    'map_e'           : {'arcsec':0.2076, 'kpc':1.2523 },
}
'''
scales['ASW0000h2m'][7022] = {
    # Pixel radius         = 12
    # Map radius           = 0.1895 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.1973 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0158 [arcsec]
    # Map radius           = 1.1427 [kpc]    H0inv=13.7
    # Map Extent           = 1.1904 [kpc]    H0inv=13.7
    # top_level_cell       = 0.0952 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    
    'map_r'           : {'arcsec':0.1895, 'kpc':1.1427 },
    'map_e'           : {'arcsec':0.1973, 'kpc':1.1904 },
}
'''
scales['ASW0000h2m'][7024] = {
    # Pixel radius         = 12
    # Map radius           = 0.2149 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2238 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0179 [arcsec]
    # Map radius           = 1.2962 [kpc]    H0inv=13.7
    # Map Extent           = 1.3502 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1080 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    
    'map_r'           : {'arcsec':0.2149, 'kpc':1.2962 },
    'map_e'           : {'arcsec':0.2238, 'kpc':1.3502 },
}
'''
scales['ASW0000h2m'][7025] = {
    # Pixel radius         = 12
    # Map radius           = 0.2135 [arcsec] Distance to center of outer pixel.
    # Map Extent           = 0.2224 [arcsec] Distance to outer edge of outer pixel.
    # top_level_cell_size  = 0.0178 [arcsec]
    # Map radius           = 1.2876 [kpc]    H0inv=13.7
    # Map Extent           = 1.3413 [kpc]    H0inv=13.7
    # top_level_cell       = 0.1073 [kpc]    H0inv=13.7
    # Number of rings      = 13
    # Number of pixels     = 489
    # Number of variables  = 494
    # Central pixel offset = 0

    'map_r'           : {'arcsec':0.2135, 'kpc':1.2876 },
    'map_e'           : {'arcsec':0.2224, 'kpc':1.3413 },
}


sc2 = {}


for asw, mod in scales.items():
    for mid, data in mod.items():
        sc2[mid] = data['map_e']['arcsec']
    
    
    
    