#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:26:32 2019

@author: emeline
"""
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings


class Move ( object ):
    def __init__ ( self , superstate ):
        self . superstate = superstate
    def move ( self , acceleration = None ):
        return SoccerAction ( acceleration = acceleration )
    def to_ball ( self ):
        return self . move ( self . superstate . ball_dir ())
    
class Shoot ( object ):
    
    def __init__ ( self , superstate ):
        self . superstate = superstate
        
    def shoot ( self , direction = None ):
        dist = self . superstate . player . distance ( self . superstate . ball )
        if dist < PLAYER_RADIUS + BALL_RADIUS :
            return SoccerAction ( shoot = direction )
        else :
            return SoccerAction ()

    def to_goal ( self , strength = None ):
        return self . shoot ( self . superstate . goal_dir )