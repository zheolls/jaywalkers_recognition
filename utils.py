def is_in_poly(point,points):
    c=0
    i=0
    j=len(points)-1
    while(i < len(points)):
        if not ((points[i][1]>point[1]) == (points[j][1]>point[1])): 
            if point[0] < (points[j][0]-points[i][0])*(point[1]-points[i][1])/(points[j][1]-points[i][1])+points[i][0]:
                c=not c
        j=i
        i=i+1
    return c


def is_walker_in_area(walker,poly):
    if  is_in_poly((walker[2],walker[3]),poly) or \
        is_in_poly((walker[2],walker[1]),poly):
        return True
    else:
        return False

def is_face_in_walker(face,walker):
    height=walker[3]-walker[1]
    width=walker[2]-walker[0]
    if face[0]>=walker[0]+width*0.2 and face[1]>=walker[1] \
        and face[2]<=walker[2]-width*0.2 and face[3]<=walker[3]-height*0.6:
        return True
    else:
        return False
