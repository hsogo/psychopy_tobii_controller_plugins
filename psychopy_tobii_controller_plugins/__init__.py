# -*- coding: utf-8 -*-


from psychopy.experiment.components import BaseComponent, Param
from os import path



class ptc_init_component(BaseComponent):
    """Initialize ptc_component"""
    categories = ['tobii_controller']
    targets = ['PsychoPy']
    thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
    iconFile = path.join(thisFolder,'ptc_init.png')
    tooltip = 'ptc_init: initialize tobii_controller'
    plugin = 'psychopy_tobii_controller'

    def __init__(self, exp, parentName, name='ptc_init', id=0, datafile="$'data/'+expInfo[\'participant\']+'.tsv'",
                 embed=False, overwrite=False, disabled=False):
        super(ptc_init_component, self).__init__(exp, parentName, name, disabled=disabled)
        self.type='ptc_init'
        self.url='https://github.com/hsogo/psychopy_tobii_controller/'

        #params
        self.order = ['name', 'id', 'datafile', 'overwrite', 'embed']
        self.params['id'] = Param(id, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='ID of Tobii eyetracker (0, 1, 2, ...)',
            label='Tobii eyetracker ID')
        self.params['datafile'] = Param(datafile, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Name of tobii_controller data file.',
            label='Tobii_controller Data File')
        self.params['overwrite'] = Param(overwrite, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If checked, existing datafile with the same name will be overwritten.',
            label='Overwrite datafile')
        self.params['embed'] = Param(embed, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If checked, event data is embeded into gaze data.',
            label='Embed event', categ='Advanced')
        
        # these inherited params are harmless but might as well trim:
        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim',
                  'saveStartStop', 'syncScreenRefresh'):
            if p in self.params:
                del self.params[p]
    
    def writeInitCode(self,buff):
        buff.writeIndented('from psychopy_tobii_controller import tobii_controller\n')
        buff.writeIndented('ptc_controller_tobii_controller = tobii_controller(win, id=%(id)s)\n' % (self.params))
        if self.params['datafile'].val != '':
            if not self.params['overwrite'].val:
                buff.writeIndented('ptc_controller_datafilename = %(datafile)s\n' % (self.params))
                buff.writeIndented('if os.path.exists(ptc_controller_datafilename):\n')
                buff.setIndentLevel(+1, relative=True)
                buff.writeIndented('raise FileExistsError(\'File exists: %s\' % ptc_controller_datafilename)\n')
                buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('ptc_controller_tobii_controller.open_datafile(%(datafile)s, embed_events=%(embed)s)\n' % (self.params))
    
    def writeFrameCode(self, buff):
        pass
    
    def writeExperimentEndCode(self, buff):
        if self.params['datafile'].val != '':
            buff.writeIndented('ptc_controller_tobii_controller.close_datafile()\n')


class ptc_cal_component(BaseComponent):
    """Run calibration"""
    categories = ['tobii_controller']
    targets = ['PsychoPy']
    thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
    iconFile = path.join(thisFolder,'ptc_cal.png')
    tooltip = 'ptc_cal: tobii_controller calibration'
    plugin = 'psychopy_tobii_controller'

    def __init__(self, exp, parentName, name='ptc_cal', show_status=True,
        calibration_points = '[[-0.4,-0.4],\n [0.4,-0.4],\n [0,0],\n [-0.4,0.4],\n [0.4,0.4]]',
        shuffle=True, enable_mouse=False, start_key='space', decision_key='space',
        text_color='white', move_duration=1.5, disabled=False):
        super(ptc_cal_component, self).__init__(exp, parentName, name, disabled=disabled)
        self.type='ptc_cal'
        self.url='https://github.com/hsogo/psychopy_tobii_controller/'
        
        #params
        self.order = ['name', 'show_status', 'calibration_points', 'shuffle', 
            'enable_mouse', 'start_key', 'decision_key', 'text_color', 'move_duration']
            
        self.params['show_status'] = Param(show_status, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Show Tobii status before calibration',
            label='Show status')
        self.params['calibration_points'] = Param(calibration_points, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[], inputType="multi", 
            hint='List of calibration points',
            label='Calibration points')
        self.params['shuffle'] = Param(shuffle, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If checked, order of calibration points is randomized.',
            label='Shuffle')
        self.params['enable_mouse'] = Param(enable_mouse, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If checked, mouse operation is enabled.',
            label='Enable mouse operation', categ='Advanced')
        self.params['start_key'] = Param(start_key, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Name of the key that is used to start calibration procedure.',
            label='Start key', categ='Advanced')
        self.params['decision_key'] = Param(decision_key, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Name of the key that is used to decide accept/retry calibration.',
            label='Decision key', categ='Advanced')
        self.params['text_color'] = Param(text_color, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Text color',
            label='Text color', categ='Advanced')
        self.params['move_duration'] = Param(move_duration, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Motion duration',
            label='Motion duration', categ='Advanced')
            
        # these inherited params are harmless but might as well trim:
        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim',
                  'saveStartStop', 'syncScreenRefresh'):
            if p in self.params:
                del self.params[p]    

    def writeRoutineStartCode(self, buff):
        if self.params['show_status'].val:
            buff.writeIndented('ptc_controller_tobii_controller.show_status(text_color=%(text_color)s, enable_mouse=%(enable_mouse)s)\n' % (self.params))
    
        buff.writeIndented('ptc_controller_tobii_controller.run_calibration(\n')
        buff.setIndentLevel(+1, relative=True)
        buff.writeIndented('calibration_points=%(calibration_points)s,\n' % (self.params))
        buff.writeIndented('shuffle=%(shuffle)s, start_key=%(start_key)s, decision_key=%(decision_key)s,\n' % (self.params))
        buff.writeIndented('text_color=%(text_color)s, enable_mouse=%(enable_mouse)s, move_duration=%(move_duration)s)\n' % (self.params))
        buff.setIndentLevel(-1, relative=True)



class ptc_rec_component(BaseComponent):
    """Recording"""
    categories = ['tobii_controller']
    targets = ['PsychoPy']
    thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
    iconFile = path.join(thisFolder,'ptc_rec.png')
    tooltip = 'ptc_rec: tobii_controller calibration'
    plugin = 'psychopy_tobii_controller'

    def __init__(self, exp, parentName, name='ptc_rec', start_rec=True, start_msg='',
                 stop_rec=True, stop_msg='', wait=True, disabled=False):
        super(ptc_rec_component, self).__init__(exp, parentName, name, disabled=disabled)
        self.type='ptc_rec'
        self.url='https://github.com/hsogo/psychopy_tobii_controller/'
        
        #params
        self.order = ['name', 'start_rec', 'start_msg', 'stop_rec', 'stop_msg', 'wait']
        self.params['start_rec']=Param(start_rec, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint="Start recording at the beginning of this routine.  Uncheck this if recording is continuing from the preceding routine.",
            label="Start Recording")
        self.params['start_msg'] = Param(start_msg, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='This text is inserted at the beginning of the recording.',
            label='Event (start)', categ='Advanced')
        self.params['stop_rec']=Param(stop_rec, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint="Stop recording at the end of this routine.  Uncheck this if you want to continue recording in the next routine.",
            label="Stop Recording")
        self.params['stop_msg'] = Param(stop_msg, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='This text is inserted at the end of the recording.',
            label='Event (stop)', categ='Advanced')
        self.params['wait'] = Param(wait, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If checked, experiment stops until data become available.',
            label='Wait for data', categ='Advanced')
            
        # these inherited params are harmless but might as well trim:
        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim',
                  'saveStartStop', 'syncScreenRefresh'):
            if p in self.params:
                del self.params[p]

    def writeRoutineStartCode(self, buff):
        if self.params['start_rec'].val:
            buff.writeIndented('ptc_controller_current_routineTimer_value = routineTimer.getTime()\n')
            buff.writeIndented('ptc_controller_tobii_controller.subscribe(wait=%(wait)s)\n' % (self.params))
            buff.writeIndented('routineTimer.reset(ptc_controller_current_routineTimer_value)\n')
            if self.params['start_msg'].val != '':
                buff.writeIndented('ptc_controller_tobii_controller.record_event(%(start_msg)s)\n' % (self.params))

    def writeFrameCode(self, buff):
        pass

    def writeRoutineEndCode(self,buff):
        if self.params['stop_rec'].val:
            if self.params['stop_msg'].val != '':
                buff.writeIndented('ptc_controller_tobii_controller.record_event(%(stop_msg)s)\n' % (self.params))
            buff.writeIndented('ptc_controller_tobii_controller.unsubscribe()\n')


class ptc_message_component(BaseComponent):
    """Recording"""
    categories = ['tobii_controller']
    targets = ['PsychoPy']
    thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
    iconFile = path.join(thisFolder,'ptc_message.png')
    tooltip = 'ptc_message: tobii_controller calibration'
    plugin = 'psychopy_tobii_controller'

    def __init__(self, exp, parentName, name='ptc_message', time='', timeType='condition',
                 text='event', sync=False, disabled=False):
        super(ptc_message_component, self).__init__(exp, parentName, name, disabled=disabled)
        self.type='ptc_message'
        self.url='https://github.com/hsogo/psychopy_tobii_controller/'
        
        #params
        self.order = ['name', 'time', 'timeType', 'text', 'sync']
        self.params['time']=Param(time, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='When this event should be recorded?',
            label='time')
        self.params['timeType']=Param(timeType, valType='str', inputType='choice',
            allowedTypes=[],
            allowedVals=['time (s)', 'frame N', 'condition'],
            updates='constant', allowedUpdates=[], 
            hint='How do you want to define time?',
            label='time type')
        self.params['text']=Param(text, valType='str', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Event text',
            label='Event')
        self.params['sync']=Param(sync, valType='bool', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='Event is recorded when the screen is flipped',
            label='Sync timing with screen')
        # these inherited params are harmless but might as well trim:
        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim',
                  'saveStartStop', 'syncScreenRefresh'):
            if p in self.params:
                del self.params[p]

    def writeRoutineStartCode(self, buff):
        buff.writeIndented('%(name)s_sent=False\n' % (self.params))

    def writeFrameCode(self, buff):
        if self.params['sync'].val:
            code = 'win.callOnFlip(ptc_controller_tobii_controller.record_event, %(text)s)\n' % (self.params)
        else:
            code = 'ptc_controller_tobii_controller.record_event(%(text)s)\n' % (self.params)

        if self.params['timeType'].val=='time (s)':
            buff.writeIndented('if %(name)s_sent==False and %(time)s<=t:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented(code)
            buff.writeIndented('%(name)s_sent=True\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
        elif self.params['timeType'].val=='frame N':
            buff.writeIndented('if %(time)s==frameN:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented(code)
            buff.setIndentLevel(-1, relative=True)
        else: # condition
            buff.writeIndented('if %(time)s:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented(code)
            buff.setIndentLevel(-1, relative=True)


class ptc_getpos_component(BaseComponent):
    """Recording"""
    categories = ['tobii_controller']
    targets = ['PsychoPy']
    thisFolder = path.abspath(path.dirname(__file__))#the absolute path to the folder containing this path
    iconFile = path.join(thisFolder,'ptc_getpos.png')
    tooltip = 'ptc_getpos: tobii_controller calibration'
    plugin = 'psychopy_tobii_controller'

    def __init__(self, exp, parentName, name='ptc_getpos', filler=-10000, 
                 binocular='Average', disabled=False):
        super(ptc_getpos_component, self).__init__(exp, parentName, name, disabled=disabled)
        self.type='ptc_getpos'
        self.url='https://github.com/hsogo/psychopy_tobii_controller/'
        
        #params
        self.order = ['name', 'start_msg', 'stop_msg']
        self.params['filler']=Param(filler, valType='code', allowedTypes=[],
            updates='constant', allowedUpdates=[],
            hint='If gaze position is not available, gaze position is filled by this value.',
            label='Filler')
        self.params['binocular']=Param(binocular, valType='str', inputType='choice', allowedTypes=[],
            allowedVals=['Average','LR'],
            updates='constant', allowedUpdates=[],
            hint='Average: (average_x, average_y) LR: {\'left\':(left_x, left_y), \'right\':(right_x, right_y)}',
            label='Binocular Data')
        # these inherited params are harmless but might as well trim:
        for p in ('startType', 'startVal', 'startEstim', 'stopVal',
                  'stopType', 'durationEstim',
                  'saveStartStop', 'syncScreenRefresh'):
            if p in self.params:
                del self.params[p]

    def writeRoutineStartCode(self, buff):
        buff.writeIndented('%(name)s = []\n\n' % self.params)

    def writeFrameCode(self, buff):
        buff.writeIndented('%(name)s = ptc_controller_tobii_controller.get_current_gaze_position()\n' % self.params)

        if self.params['binocular'] == 'LR':
            buff.writeIndented('if %(name)s[0] is np.nan:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s[0] = %(filler)s\n' % (self.params))
            buff.writeIndented('%(name)s[1] = %(filler)s\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('if %(name)s[2] is np.nan:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s[2] = %(filler)s\n' % (self.params))
            buff.writeIndented('%(name)s[3] = %(filler)s\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
        else: #average
            buff.writeIndented('if %(name)s[0] is np.nan and %(name)s[2] is np.nan:\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s = [%(filler)s, %(filler)s]\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('elif %(name)s[0] is np.nan: #left eye is not available\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s = %(name)s[2:4]\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('elif %(name)s[2] is np.nan: #right eye is not available\n' % (self.params))
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s = %(name)s[0:2]\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
            buff.writeIndented('else:\n')
            buff.setIndentLevel(+1, relative=True)
            buff.writeIndented('%(name)s = [(%(name)s[0]+%(name)s[2])/2.0,(%(name)s[1]+%(name)s[3])/2.0]\n' % (self.params))
            buff.setIndentLevel(-1, relative=True)
