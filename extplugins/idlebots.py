# Copyright (C) 2010 Gammelbob
# Inspired by the bot plugin from Beber888
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# 
#
# Changelog :
# 0.0.2 : hosted @ github


__version__ = '0.0.2'
__author__  = 'Gammelbob'


import b3, threading, time
import b3.plugin



    
#--------------------------------------------------------------------------------------------------
class IdlebotsPlugin(b3.plugin.Plugin):
    
	NameBot1 = ''
	NameBot2 = ''
	NameBot3 = ''
	NameBot4 = ''
	NameBot5 = ''
	NameBot6 = ''
	NameBot7 = ''
	NameBot8 = ''
	ConfigBot1 = ''
	ConfigBot2 = ''
	ConfigBot3 = ''
	ConfigBot4 = ''
	ConfigBot5 = ''
	ConfigBot6 = ''
	ConfigBot7 = ''
	ConfigBot8 = ''

	Name_nobm_Bot1 = ''
	Name_nobm_Bot2 = ''
	Name_nobm_Bot3 = ''
	Name_nobm_Bot4 = ''
	Config_nobm_Bot1 = ''
	Config_nobm_Bot2 = ''
	Config_nobm_Bot3 = ''
	Config_nobm_Bot4 = ''

	
	TeamListBlue = ''
	TeamListRed = ''
	PlayerInTeamBlueCount = 0
	PlayerInTeamRedCount = 0
	PlayerInTeamCount = 0
	MoveBotsToSpec = False
	botmatch = False

	min_level_botmatch_cmd = 60
	min_level_maxbots_cmd = 60

	Max_Bot = 0
	frequency_cycle = 30

	
	def onLoadConfig(self):
		self.NameBot1 = self.config.get('settings', 'name_bot1')
		self.NameBot2 = self.config.get('settings', 'name_bot2')
		self.NameBot3 = self.config.get('settings', 'name_bot3')
		self.NameBot4 = self.config.get('settings', 'name_bot4')
		self.NameBot5 = self.config.get('settings', 'name_bot5')
		self.NameBot6 = self.config.get('settings', 'name_bot6')
		self.NameBot7 = self.config.get('settings', 'name_bot7')
		self.NameBot8 = self.config.get('settings', 'name_bot8')

		self.ConfigBot1 = self.config.get('settings', 'caracteristic_bot1')
		self.ConfigBot2 = self.config.get('settings', 'caracteristic_bot2')
		self.ConfigBot3 = self.config.get('settings', 'caracteristic_bot3')
		self.ConfigBot4 = self.config.get('settings', 'caracteristic_bot4')
		self.ConfigBot5 = self.config.get('settings', 'caracteristic_bot5')
		self.ConfigBot6 = self.config.get('settings', 'caracteristic_bot6')
		self.ConfigBot7 = self.config.get('settings', 'caracteristic_bot7')
		self.ConfigBot8 = self.config.get('settings', 'caracteristic_bot8')

		self.Name_nobm_Bot1 = self.config.get('settings', 'name_nobm_bot1')
		self.Name_nobm_Bot2 = self.config.get('settings', 'name_nobm_bot2')
		self.Name_nobm_Bot3 = self.config.get('settings', 'name_nobm_bot3')
		self.Name_nobm_Bot4 = self.config.get('settings', 'name_nobm_bot4')
		self.Config_nobm_Bot1 = self.config.get('settings', 'caracteristic_nobm_bot1')
		self.Config_nobm_Bot2 = self.config.get('settings', 'caracteristic_nobm_bot2')
		self.Config_nobm_Bot3 = self.config.get('settings', 'caracteristic_nobm_bot3')
		self.Config_nobm_Bot4 = self.config.get('settings', 'caracteristic_nobm_bot4')

		self.min_level_botmatch_cmd = self.config.getint('settings', 'min_level_botmatch_cmd')
		self.min_level_maxbots_cmd = self.config.getint('settings', 'min_level_maxbots_cmd')

		self.botmatch = self.config.getboolean('settings', 'botmatch')
		self.Max_Bot = self.config.getint('settings', 'maximum_bot')
		self.frequency_cycle = self.config.getint('settings', 'frequency_cycle_in_seconds')
		self.MoveBotsToSpec = self.config.getboolean('settings', 'MoveBotsToSpec')

		# get the plugin so we can register commands
		self._adminPlugin = self.console.getPlugin('admin')
		if not self._adminPlugin:
			# something is wrong, can't start without admin plugin
			self.error('Could not find admin plugin')
		else:
			self._adminPlugin.registerCommand(self, 'botmatch', self.min_level_botmatch_cmd, self.setBotmatch)
			self._adminPlugin.registerCommand(self, 'maxbots', self.min_level_maxbots_cmd, self.setMaxBots)

	def setBotmatch(self, data, client, cmd=None):
		"""\
		<on/off> - Activates botmatch (Human vs. Bots)
		"""
		if data == 'on':
			# activating botmatch
			self.botmatch = True
			self.console.say('Botmatch is now ^2activated')
		elif data == 'off':
			# deactivating botmatch
			self.botmatch = False
			self.console.say('Botmatch is now ^9deactivated')
		else:
			# printing botmatch status
			if self.botmatch == True:
				self.console.say('Botmatch is ^2activated')
			else:
				self.console.say('Botmatch is ^9deactivated')
		return True

	def setMaxBots(self, data, client, cmd=None):
		"""\
		<count> - Server is filled with bots until this value is reached. If botmatch is active this value determines how many bots will be in the AI team.
		"""
		if data == '':
			self.console.say('Botcount currently set to %s' % (self.Max_Bot))
			return True
		else:
			try:
				self.Max_Bot = int(data)
				self.console.say('Botcount set to %s' % (self.Max_Bot))
				return True
			except:
				self.console.say('Your value \"%s\" could not be verified' % (data))
				return False

	def onStartup(self):
		self.CycliqueCheck()

	def CycliqueCheck(self):
		self.TempoCheck = threading.Timer(self.frequency_cycle, self.RegulBots)
		self.TempoCheck.start()


	def RegulBots(self):

		# perfomance boost: kick all bots if no player connected
		clist = self.console.clients.getList()
		humanplayerfound = False
		if len(clist) > 0:
			for c in clist:
				if 'BOT' not in c.guid:
					humanplayerfound = True
					break
			if humanplayerfound == False:
				for c in clist:
					if 'BOT' in c.guid:
						self.console.write('kick %s' % (c.name))
				# restart again
				self.CycliqueCheck()
				return False
		else:
			# nothing to do, just restart again
			self.CycliqueCheck()
			return False

		#self.console.write('idlebots: DEBUG uh we got an order')
		self.refreshTeamList()
		
		# check if we need to switch teams
		if self.botmatch == False and self.PlayerInTeamCount == self.Max_Bot and 'bot' in self.console.write('status'):
			if self.PlayerInTeamRedCount == 0:
				clist = self.console.clients.getList()
				#clist = self.console.clients.getClientsByLevel(0)
				if len(clist) > 0:
					for c in clist:
						if 'BOT' in c.guid:
							if self.cid2char(c.cid) in self.TeamListBlue:
								self.console.write('idlebots: DEBUG moving %s to team red' % (c.name))
								self.console.write('forceteam %s red' % (c.cid))
								self.refreshTeamList()
								break
			elif self.PlayerInTeamBlueCount == 0:
				clist = self.console.clients.getList()
				#clist = self.console.clients.getClientsByLevel(0)
				if len(clist) > 0:
					for c in clist:
						if 'BOT' in c.guid:
							if self.cid2char(c.cid) in self.TeamListRed:
								self.console.write('idlebots: DEBUG moving %s to team blue' % (c.name))
								self.console.write('forceteam %s blue' % (c.cid))
								self.refreshTeamList()
								break
		elif self.botmatch == True:
			self.console.say('Botmatch active: Red ^9[human]^7 vs. Blue ^4[AI]')
			clist = self.console.clients.getList()
			if len(clist) > 0:
				for c in clist:
					if 'BOT' not in c.guid:
						if self.cid2char(c.cid) in self.TeamListBlue:
							#self.console.write('idlebots: DEBUG moving human %s to team red' % (c.name))
							self.console.write('forceteam %s red' % (c.cid))
							self.console.say('Found human player in blue team. Moving %s to red' % (c.name))
							self.refreshTeamList()
							# we need a break here to keep our "per-tick" actions to a minimum
							break

		if self.MoveBotsToSpec == True and self.botmatch == False:
			# check if we need to force a bot from spec to team
			if self.PlayerInTeamCount < self.Max_Bot and 'bot' in self.console.write('status'):
				TeamLists = '%s%s' % (self.TeamListBlue, self.TeamListRed)
				clist = self.console.clients.getList()
				#clist = self.console.clients.getClientsByLevel(0)
				if len(clist) > 0:
					for c in clist:
						if 'BOT' in c.guid:
							if self.cid2char(c.cid) not in TeamLists:
								if self.PlayerInTeamRedCount > self.PlayerInTeamBlueCount:
									self.console.write('forceteam %s blue' % (c.cid))
									self.refreshTeamList()
									break
								else:
									self.console.write('forceteam %s red' % (c.cid))
									self.refreshTeamList()
									break

			# check if we need to force a bot from team to spec
			if self.PlayerInTeamCount > self.Max_Bot and 'bot' in self.console.write('status'):
				clist = self.console.clients.getList()
				#clist = self.console.clients.getClientsByLevel(0)
				if len(clist) > 0:
					for c in clist:
						if 'BOT' in c.guid:
							if self.PlayerInTeamRedCount > self.PlayerInTeamBlueCount:
								if self.cid2char(c.cid) in self.TeamListRed:
									self.console.write('forceteam %s s' % (c.cid))
									self.refreshTeamList()
									break
							else:
								if self.cid2char(c.cid) in self.TeamListBlue:
									self.console.write('forceteam %s s' % (c.cid))
									self.refreshTeamList()
									break
		else:
			# check if we need to kick a bot
			if self.PlayerInTeamCount > self.Max_Bot and 'bot' in self.console.write('status') and self.botmatch == False:
				clist = self.console.clients.getList()
				#clist = self.console.clients.getClientsByLevel(0)
				if len(clist) > 0:
					for c in clist:
						if 'BOT' in c.guid:
							if self.PlayerInTeamRedCount > self.PlayerInTeamBlueCount:
								if self.cid2char(c.cid) in self.TeamListRed:
									self.console.write('kick %s' % (c.name))
									break
							else:
								if self.cid2char(c.cid) in self.TeamListBlue:
									self.console.write('kick %s' % (c.name))
									break

		# check if we need to add a bot
		if self.PlayerInTeamCount < self.Max_Bot or (self.botmatch == True and self.PlayerInTeamBlueCount < self.Max_Bot):
			if self.PlayerInTeamRedCount > self.PlayerInTeamBlueCount or self.botmatch == True:
				team = 'blue'
			else:
				team = 'red'
			self.console.write('idlebots: DEBUG engine adds 1 bot to %s to reach %s Max_Bot slots [botmatch: %s]' % (team, self.Max_Bot, self.botmatch))
			if self.botmatch == False:
				if self.Name_nobm_Bot1 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.Config_nobm_Bot1, team, self.Name_nobm_Bot1))
				elif self.Name_nobm_Bot2 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.Config_nobm_Bot2, team, self.Name_nobm_Bot2))
				elif self.Name_nobm_Bot3 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.Config_nobm_Bot3, team, self.Name_nobm_Bot3))
				elif self.Name_nobm_Bot4 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.Config_nobm_Bot4, team, self.Name_nobm_Bot4))
				else:
					self.console.say('idlebots: maximum of 4 idlebots reached')
			else:
				if self.NameBot1 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot1, team, self.NameBot1))
				elif self.NameBot2 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot2, team, self.NameBot2))
				elif self.NameBot3 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot3, team, self.NameBot3))
				elif self.NameBot4 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot4, team, self.NameBot4))
				elif self.NameBot5 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot5, team, self.NameBot5))
				elif self.NameBot6 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot6, team, self.NameBot6))
				elif self.NameBot7 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot7, team, self.NameBot7))
				elif self.NameBot8 not in self.console.write('status'):
					self.console.write('addbot %s %s 110 %s' % (self.ConfigBot8, team, self.NameBot8))
				else:
					self.console.say('idlebots: maximum of 8 bots reached')

		# restart again
		self.CycliqueCheck()


	def refreshTeamList (self):
		# refresh teamcount
		try:
			self.TeamListRed = self.console.write('g_redTeamList').split('"')[3]
			self.TeamListBlue = self.console.write('g_blueTeamList').split('"')[3]
			self.PlayerInTeamRedCount = len(self.TeamListRed) - 2
			self.PlayerInTeamBlueCount = len(self.TeamListBlue) - 2
			self.PlayerInTeamCount = int(self.PlayerInTeamBlueCount + self.PlayerInTeamRedCount)
		except:
			self.console.write('DEBUG: refreshTeamList failed')
		#self.console.write('Team Blue: %s (%s players)' % (self.TeamListBlue, self.PlayerInTeamBlueCount))
		#self.console.write('Team Red: %s (%s players)' % (self.TeamListRed, self.PlayerInTeamRedCount))

	def cid2char (self, cid):
		# convert clientids in chars for matching the g_red/g_blueteamlist pattern
		Value = ''
		if cid == '0':
			Value = 'A'
		elif cid == '1':
			Value = 'B'
		elif cid == '0':
			Value = 'C'
		elif cid == '2':
			Value = 'D'
		elif cid == '3':
			Value = 'E'
		elif cid == '4':
			Value = 'F'
		elif cid == '5':
			Value = 'G'
		elif cid == '6':
			Value = 'H'
		elif cid == '7':
			Value = 'I'
		elif cid == '8':
			Value = 'J'
		elif cid == '9':
			Value = 'K'
		elif cid == '10':
			Value = 'L'
		elif cid == '11':
			Value = 'M'
		elif cid == '12':
			Value = 'N'
		elif cid == '13':
			Value = 'O'
		elif cid == '14':
			Value = 'P'
		elif cid == '15':
			Value = 'Q'
		elif cid == '16':
			Value = 'R'
		elif cid == '17':
			Value = 'S'
		elif cid == '18':
			Value = 'T'
		elif cid == '19':
			Value = 'U'
		elif cid == '20':
			Value = 'V'
		elif cid == '21':
			Value = 'W'
		elif cid == '22':
			Value = 'X'
		elif cid == '23':
			Value = 'Y'
		elif cid == '24':
			Value = 'Z'
		return Value

