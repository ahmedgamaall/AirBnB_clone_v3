#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.engine import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())
print(storage.all())
print("First state: {}".format(storage.get(State, first_state_id)))
