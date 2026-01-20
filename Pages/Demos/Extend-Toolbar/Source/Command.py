# SPDX-License-Identifier: <License Identifier>
# SPDX-FileNotice: Part of the <Addon Name> addon.


class Command:

    def GetResources ( self ):
        return {
            'MenuText' : 'Command' ,
            'ToolTip' : 'Logs a debug message.' ,
            'Pixmap' : ''
        }

    def Activated ( self ):

        print('Command::Activated')
