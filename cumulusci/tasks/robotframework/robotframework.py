from cumulusci.tasks.salesforce import BaseSalesforceTask
from robot.run import run

class Robot(BaseSalesforceTask):
    task_options = {
        'suites': {
            'description': 'Paths to test case files/directories to be executed similarly as when running the robot command on the command line.',
            'required': True,
        },
        'test': {
            'description': 'Run a specific test by name',
        },
        'include': {
            'description': 'Includes tests with a given tag',
        },
        'exclude': {
            'description': 'Excludes tests with a given tag',
        },
        'vars': {
            'description': 'Pass values to override variables in the format VAR1:foo,VAR2:bar',
        },
        'options': {
            'description': 'A dictionary of options to robot.run method.  See docs here for format.  NOTE: There is no cci CLI support for this option since it requires a dictionary.  Use this option in the cumulusci.yml when defining custom tasks where you can easily create a dictionary in yaml.',
        },
    }

    def _init_options(self, kwargs):
        super(Robot, self)._init_options(kwargs)

        # Initialize the vars list and add the org name to it
        if 'vars' in self.options:
            if not isinstance(self.options['vars'], list):
                new_vars = []
                for var in self.options['vars'].split(','):
                    new_vars.append(var.strip())
                self.options['vars'] = new_vars
        else:
            self.options['vars'] = []
        self.options['vars'].append('ORG:{}'.format(self.org_config.name))

        # Initialize options as a dict
        if 'options' not in self.options:
            self.options['options'] = {}

    def _run_task(self):
        options = self.options['options'].copy()
        if 'test' in self.options:
            options['test'] = self.options['test']
        if 'include' in self.options:
            options['include_tag'] = self.options['include']
        if 'exclude' in self.options:
            options['exclude_tag'] = self.options['exclude']

        run(
            self.options['suites'], 
            variable=self.options['vars'],
            **self.options['options']
        )