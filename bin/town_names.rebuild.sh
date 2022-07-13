#!/bin/bash

./town_names proportions english > english_proportions.json
mv english_proportions.json ../api/town_names/data/english_proportions.json

./town_names proportions irish > irish_proportions.json
mv irish_proportions.json ../api/town_names/data/irish_proportions.json

./town_names proportions scottish > scottish_proportions.json
mv scottish_proportions.json ../api/town_names/data/scottish_proportions.json

./town_names proportions welsh > welsh_proportions.json
mv welsh_proportions.json ../api/town_names/data/welsh_proportions.json
