# Color-color diagram

![color-color](cc.png)

In X-ray astronomy we usually define "color" as the hardness ratio.  

The hardness ratio is the ratio of the difference in the 
number of counts in two independent energy bands divided by the
total number of counts.  The total number of counts may be the sum of
the two energy bands, or may be the total over a wider energy range
that full encloses the bands being used.

Thus defined, the hardness ratio will be between -1 and 1.   Values closer
to -1 are "soft", low energy band dominates.  Values closer to 1 are "hard",
high energy band dominates.

A color-color plot then shows the hardness ratio in 1 pair of 
energy bands along the X-axis, and a different pair of energy bands 
along the Y-axis.

This collection of classes simulates a spectrum with the user 
specified spectral model and instrument response.  Two of the model parameters
are varied over an input grid and the color in the different 
energy bands is computed.  This grid is then plotted in the color-color
diagram.

The idea is that for a source, if you compute the colors and assume a 
spectral model shape, you can get an estimate of the model **parameters** 
by looking at the color-color diagram.

These routines are dependent on [Sherpa](http://cxc.cfa.harvard.edu/sherpa)
for the models. Plotting is done using matplotlib.


## Examples

### Command line tool

The plot shown above was created using the following command line

```bash
$ color_color acis.arf clr.fits mode=h showplot=yes outplot=clr.png \
    model="xsphabs.abs1*xspowerlaw.pwrlaw" \
    param1=pwrlaw.PhoIndex \
    grid1=1,2,3,4 \
    param2=abs1.nH \
    grid2=0.01,0.1,0.2,0.5,1,10 \
    soft=csc medium=csc hard=csc \
    clobber=yes
```

The values are also stored in the output file `clr.fits`

```bash
$ dmlist clr.fits cols
 
--------------------------------------------------------------------------------
Columns for Table Block TABLE
--------------------------------------------------------------------------------
 
ColNo  Name                 Unit        Type             Range
   1   PhoIndex                          Real8          -Inf:+Inf            
   2   nH                                Real8          -Inf:+Inf            
   3   S_COUNTS                          Real8          -Inf:+Inf            
   4   M_COUNTS                          Real8          -Inf:+Inf            
   5   H_COUNTS                          Real8          -Inf:+Inf            
   6   HARD_HM                           Real8          -Inf:+Inf            
   7   HARD_MS                           Real8          -Inf:+Inf            
```



### `Python` module

```python
from color_color import *

import sherpa.astro.ui as ui

#
# Define our energy bands
#
soft = EnergyBand( 0.5, 1.2, 'S')
medium = EnergyBand(1.2, 2.0, 'M')
hard = EnergyBand(2.0, 7.0, 'H')

#
# Define model
#
mymodel = ui.xswabs.abs1 * ui.xspowerlaw.pwrlaw
arffile = "acissD2006-10-26pimmsN0009.fits"

#
# First model parameter axis
#
pho_grid = [ 1., 2., 3., 4. ]
photon_index = ModelParameter( pwrlaw.PhoIndex, pho_grid)

#
# Second model parameter axis
# 
sg = [ 1.e20, 1.e21, 2.e21, 5.e21, 1.e22, 1e23] 
nh_grid = [x/1e22 for x in sg ]
absorption = ModelParameter( abs1.nH, nh_grid)

#
# Get to work.  
#
hm_ms = ColorColor( mymodel, arffile )
hm_ms_results = hm_ms( photon_index, absorption, soft, medium, hard)

#
# Setup plot styles
#
photon_index.set_curve_style(marker="", color="black" )
absorption.set_curve_style(marker="", linestyle="--", color="forestgreen") 
absorption.set_label_style(color="forestgreen")

hm_ms_results.plot("color_color.png")

vals = hm_ms_results.get_results()
```

The output looks like

![color-color diagram](color_color.png)


Now suppose there was a source with `(H-M)=-0.25` and `(M-S)=-0.2`.
If the assumption about the spectral model is correct, then it would 
be expected to have a photon index between 2 and 3 and absorption between 0.2 and 0.5
e10^22.

## Total energy band

If the total energy band is `None` then the routines will use the sum of
the individual bands independently for each axis.  In this case the 
color values will fill the entire -1:1 parameter space.

If the total energy band is specified, then it may be the case that only
part of the parameter space is filled. 


## Background

Background is not treated specifically with these routines, but you can
include the background term in the model expression, something like

```python
mymodel = ui.xswabs.abs1 * ui.xspowerlaw.pwrlaw + ui.const1d.bkg
bkg.c0 = 0.01
```

to see how it affects things.  The background model component 
can be as complicated as needed.

