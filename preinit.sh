#! /bin/sh
#
# init.sh
# Copyright (C) 2023 jared <jared@JARED-STUDIO>
#
# Distributed under terms of the MIT license.
#


sqlite3 src/data.db < schema.sql
sqlite3 src/data.db < init.sql
