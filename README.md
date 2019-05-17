Datadog Symfony Vulnerabilities
=================================

Adds a check to Datadog which checks local installed Symfony installation(s) for vulnerabilities.

This check is performed using the composer.lock file in combination with SensioLabs Security Advisories Checker API.

Visit https://security.symfony.com for a complete list of supported packages for this API.

Be aware the composer.lock file is uploaded to the above mentioned API, so make sure the file does not contain information you don't want to be uploaded to this API.

The metric returned to Datadog contains a numeric value of the total amount of known vulnerabilities. This means only value `0` is a positive outcome.

Requirements
------------

Datadog Agent should be installed. Composer.lock file with supported packages by SensioLabs Security Advisories Checker API. 

Role Variables
--------------

Below is a list of default values along with a description of what they do.

```
# path to one or more composer.lock files
dwv_composer_lock_files:
  - /srv/www/example.com/current/symfony/composer.lock
  - /srv/www/example.com/current/drupal/composer.lock

# path where Datadog Agent stores its checks, this is the default directory
dwv_datadog_checks_path: /etc/dd-agent/checks.d

# path where Datadog Agent stores its configurations, this is the default directory
dwv_datadog_conf_path: /etc/dd-agent/conf.d

# interval for this check to run, it will run as often as the specified interval (in seconds)
dwv_datadog_check_interval: 3600
```

Example Playbook
----------------

```
datadog-symfony-vulnerabilities:
    - dwv_composer_lock_files:
        - /srv/www/example.com/current/symfony/composer.lock
        - /srv/www/example.com/current/drupal/composer.lock
    - dwv_datadog_check_interval: 3600
```

Remove Playbook
---------------

To remove this playbook remove the following files from the server and restart datadog-agent:

- `/etc/dd-agent/checks.d/symfony_vulnerabilities.py`
- `/etc/dd-agent/checks.d/symfony_vulnerabilities.pyc`
- `/etc/dd-agent/conf.d/symfony_vulnerabilities.conf`

Troubleshooting
---------------

When something is not working you can perform the following checks:

- Update Datadog Agent to the latest release
- Make sure the path to the composer.lock file is correct
- Visit `https://security.symfony.com/check` and upload the composer.lock file and see if this is working correctly
- Run `sudo /etc/init.d/datadog-agent info` to see if the check is running and if it shows any errors
- Use the Datadog Metrics Explorer to check if the metric is available and what it's value is

Note
----

This Datadog check is as basic as possible to prevent the need for new dependencies.

If you don't mind dependencies you can modify this check to make use of the SensioLabs Security Checker CLI tool (see https://github.com/sensiolabs/security-checker). And for example the Python `requests` module can accomplish most of this script in just a few lines, but is not installed by default.

License
-------

BSD

Author Information
------------------

See https://www.erikdevries.com or https://github.com/edv for more information
