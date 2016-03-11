# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse
import dateutil.parser
import ephem
import math

def _format_position(deg):
    the_minus = ""
    if deg < 0:
        the_minus = "-"
    g = int(math.degrees(deg))
    m = (math.degrees(deg)-g)*60
    gm = u"%s%s°%04.1f"%(the_minus,abs(g),abs(m))

def gp(request):

    if request.GET:
        try:
            dt = request.GET['date_time']
            latlong_format = request.GET['format']

            dt = dateutil.parser.parse(dt)

            sun = ephem.Sun()
            obs = ephem.Observer()
            obs.date = dt
            sun.compute(dt,epoch=dt)


            gha = str(ephem.degrees(obs.sidereal_time()-sun.g_ra).norm)
            declination = str(sun.dec)

            import pdb; pdb.set_trace();
            if 'degrees' == latlong_format:
                declination = _format_position(declination)
                gha = _format_position(gha)

            return JsonResponse({'declination': declination,
                                 'gha': gha
            })

        except:
            return JsonResponse({})
        
        data = {'one': 1}
        return JsonResponse(data)

    else:
        return JsonResponse({})
