"""
Author: Benjamin Nie
Date: 2014-Sept-05






Description:

    This python file contains two methods:

    1. is_angle_between(input_angle, bound1, bound2)
        Method returns True when input_angle is within bounds of the angle formed by bound1 and bound2 (with chosen angle <= 180 degrees)

    2. are_coords_within_distance(dist, coord1, coord2)
        Return whether a GPS coordinate coord1 (in decimal form) is less than or equal to distance dist (in meters) from another GPS coordinate coord2.  Use 6,378,100 for radius of the earth in meters.






Explanation of Design:

    1. is_angle_between(input_angle, bound1, bound2)
        - Did not use Python's math library due to the computational and time expense.  Though it would make the code more readable (ex. using absolute values instead of checking for both positive and negative values), the tradeoff would be an increase in computation time, which the Sailbot may not be able to afford due to it's time-sensitive decision making requirements.

        - Adding to the previous point, also didn't use Python's math library for trignometric functions in fear of computational expenses for the same reason stated above

        - I am convinced there is a more elegant way to solve this problem using vectors and linear algebra without introducing the computationally expensive trignometric functions.  I researched Convex Hull algorithms, which look very promising.  However, due to time restraints and unfamiliarity with the Convex Hull algorithm, I could not finish writing the solution using that method.  If given more time, I believe this would be the best solution both in terms of code
          readability and code performance.

    2. are coords_within_distance(dist, coord1, coord2)
        - GPS coordinates require both longitude and latitude.  To incorporate both values into a single argument, I used a Python tuple to hold latitude in the 0th element and longitude in the 1st element.  Other containers, such as lists or sets, could have been used as well, but the complexity of those containers are not necessary for a simple task such as this.

        - The algorithm I used (Haversine) to calculate the distance between two GPS coordinates heavily uses functions found within Python's math library.  Though this is not ideal due to the heavy computational expense, this is the best solution I've found thus far.  On the bright side, the code is very readable and there is very little complexity in the logic of this method.







End Notes:
    - For testing, Python's unittest module would be the ideal testing framework.  I've been using the tool at work over the last 8 months and it is very robust, scalable, with lots of documentation and support found online.  Did not incorporate unittest since it will require a few more Python files, which violates the requirement of a single Python file for submission

    - Further experimentation can be carried out to determine if the computational expenses incurred by using  Python's math library will affect the overall dynamics of the boat.  If the computational expense is insigificant, the code within this function can be refactored by incoporating Python's math functions for easier readability and future maintenance.  These computational expenses also heavily depend on the microprocessor power of our           microcontroller, which I believe is
              currently in transition from an Arduino to a PIC32

    - A good profiling tool (to determine how long a portion of code takes to run) for C is GCOV.  A similar tool for Python should exist, and would be a great way to test computational expenses for the Python math library

    - All development and testing were done using Python v2.6 on a Linux Fedora distro
"""

import math

"""
Determines if the GPS coordinates of coord1 is less than or equal to the distsance dist (in meters) from another GPS coordinate coord2.  6,378,100 (meters) is used as the radius of the earth.

@param:
    1. dist - Integer.  Distance that is used for comparison
    2. coord1 - Tuple of Integers.  GPS coordinate of location one in decimal form.  0th element is latitude and 1st element is longitude.
    3. coord2 - Tuple of Integers.  GPS coordinate of location two in decimal form.  0th element is latitude and 1st element is longitude.

@return:
    1. True - If distance between coord1 and coord2 is lesser than or equal to than argument dist
    2. False - If distance between coord1 and coord2 is greater than argument dist
"""
def are_coords_within_distance(dist, coord1, coord2):

    lat1 = coord1[0]
    long1 = coord1[1]
    lat2 = coord2[0]
    long2 = coord2[1]

    # implementing haversine formula to calculate distance between two surface points on a sphere
    dlong = math.radians(long2 - long1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlong/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Finding distance in meters between two points
    dist_coord1_coord2 = 6378100 * c

    # Determine if distance between coord1 and coord2 are <= dist variable passed in as parameter
    if dist > dist_coord1_coord2:
        print ("The distance between coord1 and coord2 is ") + str(dist_coord1_coord2) + (", which is less than the distance of ") + str(dist) + (" that was passed into this method as an argument")
        return True

    else:
        print ("The distance between coord1 and coord2 is ") + str(dist_coord1_coord2) + (", which is greater than the distance of ") + str(dist) + (" that was passed into this method as an argument")
        return False

"""
Determines if the input_angle is bound by the smaller acute angle formed between bound1 and bound2

@param:
    1. input_angle - Integer.  Angle of interest
    2. bound1 - boundary angle 1
    3. bound2 - boundary angle 2

@return:
    1. True - If input_angle is bound by smaller acute angle formed between bound1 and bound 2
    2. False - If input_angle is not bound by smaller acute angle formed between bound1 and bound 2
"""
def is_angle_between(input_angle, bound1, bound2):

    # bound1 and bound2 are 180 or 0 degrees apart - no existence of a smaller angle
    if (bound1 - bound2) == 0 or (bound1 - bound2) == 180 or (bound1 - bound2) == -180:
        print ("bound1 ") + str(bound1) + (" and bound2 ") + str(bound2) + (" are parallel and no smaller angle exists between them")
        return False

    # input angle shares angle with bound1 or bound2
    if input_angle == bound1 or input_angle == bound2:
        print ("The input angle ") + str(input_angle) + (" is right on a boundary and is therefore contained within bound")
        return True

    # convert all angles into positive values
    pos_input_angle, pos_bound1, pos_bound2 = convert_to_positive_angle(input_angle, bound1, bound2)

    # assign bound1 and bound2 to high_angle and low_angle variables
    high_angle, low_angle = assign_high_and_low_angles(pos_bound1, pos_bound2)

    # smaller angle is formed starting from low_angle and going ccw towards high_angle
    if (high_angle - low_angle) <= 179:

        if low_angle <= pos_input_angle <= high_angle:
            print ("Angle ") + str(input_angle) + (" is contained within bound 1 ") + str(bound1) + (" and bound 2 ") + str(bound2)
            return True

        else:
            print ("Angle ") + str(input_angle) + (" is not contained within bound 1 ") + str(bound1) + (" and bound 2 ") + str(bound2)
            return False

    # smaller angle is formed starting from low_angle and going cw towards high_angle
    elif (high_angle - low_angle) > 179:

        if low_angle <= pos_input_angle <= high_angle:
            print ("Angle ") + str(input_angle) + (" is not contained within bound 1 ") + str(bound1) + (" and bound 2 ") + str(bound2)
            return False

        else:
            print ("Angle ") + str(input_angle) + (" is contained within bound 1 ") + str(bound1) + (" and bound 2 ") + str(bound2)
            return True

    else:
        print ("Error has occured")
        return False

"""
Converts all negative angles in unit circle into their corresponding positive angles

@param:
    1. input_angle
    2. bound1
    3. bound2

@return:
    Positive values of all angles
"""
def convert_to_positive_angle(input_angle, bound1, bound2):
    if input_angle < 0:
        input_angle += 360

    if bound1 < 0:
        bound1 += 360

    if bound2 < 0:
        bound2 += 360

    return input_angle, bound1, bound2

"""
Determines the numerical higher and lower angles between bound1 and bound2

@param:
    1. bound1
    2. bound2

@return:
    The numerically higher and lower angles
"""
def assign_high_and_low_angles(bound1, bound2):
    if bound1 > bound2:
        return bound1, bound2

    elif bound2 > bound1:
        return bound2, bound1

"""
Main function.  In this case, purely used to test user methods

@param:
    None

@return:
    None
"""
if __name__ == "__main__":

    print ("\nTesting is_angle_between method\n")

    print ("Testing positive values")

    # not contained
    is_angle_between(100, 90, 80)
    # not contained
    is_angle_between(80, 90, 100)
    # contained
    is_angle_between(90, 80, 100)

    print ("\nTesting negative values")

    # not contained
    is_angle_between(-100, -90, -80)
    # not contained
    is_angle_between(-80, -90, -100)
    # contained
    is_angle_between(-90, -80, -100)

    print ("\nTesting boundary conditions")

    # parallel
    is_angle_between(0, 0, 0)
    # parallel
    is_angle_between(-180, -180, -180)
    # parallel
    is_angle_between(25, 180, 0)
    # parallel
    is_angle_between(15, 10, -170)
    # input angle aligned with boundary
    is_angle_between(179, 179, -180)

    print ("\nTesting other conditions")

    # contained
    is_angle_between(-132, 97, -112)
    # not contained
    is_angle_between(18, -177, 29)
    # not contained
    is_angle_between(140, -170, 160)
    # contained
    is_angle_between(0, 128, -20)
    # contained
    is_angle_between(5, 9, -170)
    # not contained
    is_angle_between(5, 11, -170)
    # contained
    is_angle_between(12, 11, -170)

    print ("\n\n\n\n\n\n\n\nTesting are_coords_within_distance method\n")

    print ("Testing far distance accuracy:")

    # Vancouver to Sydney
    # Expected Value: 12493000 m and less than dist
    # Source: Google Maps
    print ("\nVancouver to Sydney")
    are_coords_within_distance(100000000, (49.25, -123.1), (-33.86, 151.21))

    print ("\nTesting medium distance accuracy:")
    # Vancouver to Calgary
    # Expected Value: 675060 m and greater than dist
    # Source: http://www.mapcrow.info/Distance_between_Calgary_CA_and_Vancouver_CA.html
    print ("\nVancouver to Calgary")
    are_coords_within_distance(40000, (49.25, -123.1), (51.05, -114))

    print ("\nTesting short distance accuracy:")
    # Seattle to Tacoma
    # Expected Value: 42000 m and greater than dist
    # Source: http://www.timeanddate.com/worldclock/distanceresult.html%3Fp1=234&p2=391
    print ("\nSeattle to Tacoma")
    are_coords_within_distance(40000, (47.6097, -122.333056), (47.2414, -122.4594))

    print ("\nTesting North of equator to south of equator:")
    # London to Johannesburg
    # Expected Value: 9038000 m and less than dist
    # Source: http://www.timeanddate.com/worldclock/distances.html?n=111
    print ("\nLondon to Johannesburg")
    are_coords_within_distance(800000000, (51.51, -0.1257), (-26.20, 28.04))
