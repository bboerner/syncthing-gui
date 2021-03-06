#!/usr/bin/env python2
"""
Syncthing-GTK - DaemonSettingsDialog

Universal dialog handler for all Syncthing settings and editing
"""

from __future__ import unicode_literals
from gi.repository import Gtk, Gdk
from syncthing_gtk import EditorDialog
_ = lambda (a) : a

VALUES = [ "vListenAddress", "vLocalAnnEnabled", "vUPnPEnabled",
		"vStartBrowser", "vMaxSendKbpsEnabled", "vMaxSendKbps",
		"vURAccepted", "vLocalAnnPort", "vGlobalAnnEnabled",
		"vGlobalAnnServer"
		]


class DaemonSettingsDialog(EditorDialog):
	def __init__(self, app):
		EditorDialog.__init__(self, app, "daemon-settings.glade",
			"Syncthing Daemon Settings")
	
	#@Overrides
	def get_value(self, key):
		if key == "ListenAddress":
			return ",".join([ x.strip() for x in self.values[key]])
		elif key == "MaxSendKbpsEnabled":
			return (self.values["MaxSendKbps"] != 0)
		else:
			return EditorDialog.get_value(self, key)
	
	#@Overrides
	def set_value(self, key, value):
		if key == "ListenAddress":
			self.values[key] = [ x.strip() for x in value.split(",") ]
		elif key == "URAccepted":
			self.values[key] = 1 if value else 0
		elif key == "MaxSendKbpsEnabled":
			if value:
				if self.values["MaxSendKbps"] <= 0:
					self.values["MaxSendKbps"] = 1
			else:
				self.values["MaxSendKbps"] = 0
			self.find_widget_by_id("vMaxSendKbps").get_adjustment().set_value(self.values["MaxSendKbps"])
		else:
			return EditorDialog.set_value(self, key, value)

	#@Overrides
	def on_data_loaded(self):
		self.values = self.config["Options"]
		self.checks = {}
		return self.display_values(VALUES)
	
	#@Overrides
	def update_special_widgets(self, *a):
		self["vMaxSendKbps"].set_sensitive(self.get_value("MaxSendKbpsEnabled"))
		self["lblvLocalAnnPort"].set_sensitive(self.get_value("LocalAnnEnabled"))
		self["vLocalAnnPort"].set_sensitive(self.get_value("LocalAnnEnabled"))
		self["lblvGlobalAnnServer"].set_sensitive(self.get_value("GlobalAnnEnabled"))
		self["vGlobalAnnServer"].set_sensitive(self.get_value("GlobalAnnEnabled"))
	
	#@Overrides
	def on_save_reuqested(self):
		self.store_values(VALUES)
		# Post configuration back to daemon
		self.post_config()
	
	#@Overrides
	def on_saved(self):
		self.close()
