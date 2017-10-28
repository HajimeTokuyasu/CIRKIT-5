#!/usr/bin/env python
# coding UTF-8

import yaml

import rospy
from goal_sender_msgs.srv import ApplyGoals
from goal_sender_msgs.msg import GoalSequence
from goal_sender_msgs.msg import Waypoint

def read_yaml(path):
    f = open(path, 'r')
    waypoints = yaml.load(f)
    f.close()
    return waypoints

def get_waypoints():
    sequence = GoalSequence()
    for waypoint_data in read_yaml(rospy.get_param('~path', 'waypoints.yaml')):
        waypoint = Waypoint(name = waypoint_data.get('name', ""),
                            x = waypoint_data['x'], # required
                            y = waypoint_data['y'], # required
                            radius = waypoint_data['radius'], # required
                            importance = waypoint_data.get('importance', 0),
                            drag = waypoint_data.get('drag', 0))
        sequence.waypoints.append(waypoint)
    return sequence

if __name__ == '__main__':
    rospy.init_node('yaml_reader', anonymous=True)
    goal_sequence = get_waypoints()
    rospy.wait_for_service('apply_goals')
    try:
        apply_goals = rospy.ServiceProxy('apply_goals', ApplyGoals)
        resp = apply_goals(goal_sequence)
        print resp.message
    except rospy.ServiceException, e:
        print e