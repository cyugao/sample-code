import pymap3d as pm

API_KEY = "pk.eyJ1IjoiZ2N5MTk5OCIsImEiOiJjazQ3aWkxOWswdjZwM2txN2hjM2FnN2EyIn0.28FMNC2JbHYm3DMRoooyYQ"

import geocoder

g = geocoder.mapbox("San Francisco, CA", key=API_KEY)
g.json

lat0, lon0, h0 = -89.384172, 43.074706, 0

