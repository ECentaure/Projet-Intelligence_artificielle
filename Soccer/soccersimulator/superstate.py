#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:38:45 2019

@author: emeline
"""
from tools import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings

class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player ):
        self . state = state
        self . id_team = id_team
        self . id_player = id_player
    @property
    def ball ( self ):
        return self . state . ball . position
    @property
    def player ( self ):
        return self . state . player_state ( self . id_team , self . id_player ). position
    @property
    def goalAdv ( self ):
        return Vector2D((2 - self.id_team )*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
    @property
    def goal ( self ):
        return Vector2D((self.id_team - 1)*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)