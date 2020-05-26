# EMACS settings: -*-  tab-width: 2; indent-tabs-mode: t -*-
# vim: tabstop=2:shiftwidth=2:noexpandtab
# kate: tab-width 2; replace-tabs off; indent-width 2;
# =============================================================================
#               __  __      _         ____ _
#   _ __  _   _|  \/  | ___| |_ __ _ / ___| | __ _ ___ ___  ___  ___
#  | '_ \| | | | |\/| |/ _ \ __/ _` | |   | |/ _` / __/ __|/ _ \/ __|
#  | |_) | |_| | |  | |  __/ || (_| | |___| | (_| \__ \__ \  __/\__ \
#  | .__/ \__, |_|  |_|\___|\__\__,_|\____|_|\__,_|___/___/\___||___/
#  |_|    |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Python module:      A collection of MetaClasses for Python.
#
# Description:
# ------------------------------------
#		TODO
#
# License:
# ============================================================================
# Copyright 2017-2019 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
__api__ = [
	'Singleton',
]
__all__ = __api__


class Singleton(type):
	"""Implements a singleton pattern in form of a Python metaclass (a class constructing classes)."""

	_instanceCache = {}       #: Cache of all created singleton instances.

	def __call__(cls, *args, **kwargs):
		"""
		Overwrites the ``__call__`` method of parent class :py:class:`type` to return
		an object instance from an instances cache (see :attr:`_instanceCache`) if
		the class was already constructed before.
		"""
		if cls not in cls._instanceCache:
			cls._instanceCache[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instanceCache[cls]

	@classmethod
	def Register(cls, t, instance):
		"""Register a type,instance pair in :attr:`_instanceCache`."""

		if t not in cls._instanceCache:
			cls._instanceCache[t] = instance
		else:
			raise KeyError("Type '{type!s}' is already registered.".format(type=t))
