====================
Application Security
====================
The GlobaLeaks software conforms to industry standard best practices for application security by following `OWASP Security Guidelines <https://www.owasp.org>`_.

GlobaLeaks is made up of two main software components: a Backend and a Client

* The Backend is a python backend that runs on a physical backend and exposes a REST API which the Client interacts with.
* The Client is a client side web application that interacts with Backend only through XHR.

Key Concepts
============
This section explains the key security concepts when a Whistleblower submits a Report to a number of Recipients through GlobaLeaks.

Report
------
A report is a submission created by a Whistleblower stored in the Backend’s database.

A report is composed by the following elements:

* Questionnaire’s answers – structured and unstructured answers to the submission questionnaire;
* Files – constrained to a max size by the Administrator;
* Comments – text written by either the Whistleblower or by the recipients, which is visible to all the Recipients and to the Whistleblower;
* Messages – one to one messages between the Whistleblower and a Recipient;
* Metadata – including for example the time of Report creation, date of last access by users, number of views, number of files etc.

After a configurable amount of time a Report expires and is deleted and securely overwritten by the Backend. After deletion neither the Recipients or the Whistleblower are able to access the Report..

As well after a configurable amount of time since the last access to the Report, the Whistleblower loses the possibility to access its own report.

Whistleblower Interactions with the Platform
--------------------------------------------
A Whistleblower can access the platform, read and fill the submission questionnaire filing a report and eventually attaching evidence of the fact reported.

Every time a Whistleblower performs a new Submission on a GlobaLeaks platform a Report is created and the Whistleblower is given a randomly generated receipt. This Receipt is an authentication secret composed by 16 digits (e.g: 5454 0115 3135 3982) that acting as an anonymous authentication password lets Whistleblowers access their own Reports.

Recipient Interactions with the Platform
----------------------------------------
Any time a Report is submitted by a Whistleblower, Recipients are notified via email and they could then access the report by clicking on a link and inserting their own personal password.
Alternatively the user can access the platform via the Login interface and then access the lists of existing Reports.

When Recipients view a Report, they see the could read answers to the submission questionnaire, access the evidences attached and read some of the metadata collected by the platform like for example information about the time of the submission and the possible further communication.

If Recipients has configured a PGP encryption key then every notification sent by the platform to Recipients will be encrypted with their public key.

Authentication
==============
This section describes the authentication possibilities implemented by the system.

Due to the fact that the Backend may be deployed to be accessible via a Tor Onion Service and via HTTPS, the authentication endpoints for each user role may vary depending on the configuration.

Authentication Matrix
---------------------
The table below summarizes the authentication methods for each user role.

.. csv-table::
   :header: "User type", "Authentication method"

   "Administrator", "Username and password"
   "Recipient", "Username and password"
   "Whistleblower", "Receipt"

Authentication Methods
----------------------
Supported authentication methods are described as follows.

Password
^^^^^^^^
By accessing the GlobaLeaks login interface, Administrators and Recipients need to insert their respective username and password. If the password submitted is valid, the system grants access to the functionality available to that user.

Receipt
^^^^^^^
Whistleblowers access their Reports by using a Receipt, which is a randomly generated 16 digits sequence created by the Backend when the Report is first submitted. The reason of this format of 16 digits is that it resembles a standard phone number, making it easier for the whistleblower to conceal the receipt of their submission and give them plausible deniability on what is the significance of such digits.

Password Security
=================
The following password security measures implemented by the system.

Authentication Security
-----------------------
The confidentiality of the transmission of authentication secrets is protected by either Tor Onion Services v3 or TLS version 1.2+

Password Storage
----------------
Password are never stored in plaintext but the system maintain at rest only an hash. This apply to every authentication secret included whistleblower receipts.

The platform stores Users’ passwords hashed with a random 128 bit salt, unique for each user.

Passwords are hashed using `Argon2 <https://en.wikipedia.org/wiki/Argon2>`_, a key derivation function that was selected as the winner of the ``Password Hashing Competition`` in July 2015.

The hash involves a per-user salt for each user and a per-system salt for each whistleblower.

Password Strength
-----------------
The system enforces the usage of complex password by implementing a custom algorithm necessary for ensuring a reasonable entropy of each authentication secret.

Password are scored in three levels: strong, acceptable, unusable.
A strong password should be formed by capital letters, lowercase letters, numbers and a symbols, be at least 12 characters long and include a variety of at least 10 different inputs.
An acceptable password should be formed by at least 3 different inputs over capital letters, lowercase letters, numbers and a symbols, be at least 10 characters and include a variety of at least 7 different inputs.

Two Factor Authentication (2FA)
-------------------------------
Users are enabled to enroll for Two Factor Authentication via their own preferences.
The system implements Two Factor Authentication (2FA) based on TOTP as for `RFC 6238 <https://tools.ietf.org/rfc/rfc6238.txt>`_.

Password Change on First Login
------------------------------
The system enforces users to change their own password at their first login.
Administrators could as well enforce password change for users at their next login.

Periodic Password Change
------------------------
By default the system enforces users to change their own password at least every year.
This period is configurable by administrators.

Proof of Work on Login and Submissions
--------------------------------------
The  system implements an automatic proof of work on every login that requires every client to request a token, solve a computational probelm before being able to perform a login or file a submission.

Slowdown on Failed Login Attempts
---------------------------------
The system identifies multiple failed login attempts and implement a slowdown procedure where an authenticating client should wait up to 42 seconds to complete an authentication.
This feature is intended to slow down possible attacks requiring more resources to users in terms of time, computation and memory.

Password Recovery
-----------------
In case of password loss users could request a password reset via the web login interface ckicking on a “Forgot password?” button.
When this button is clicked, users are invited to enter their username or an email. If the provided username or the email correspond to an existing user, the system will provide a reset link to the configured email.
By clicking the link received by email the user is then invited to configure a new email different from the previous.

In case encryption is enabled on the system, a user clicking on the reset link would have first to insert their ``Account Recovery Key`` and only in case of correct insertion the user will be enabled to set a new password.

In case 2FA is enabled on the system, a user clicking on the reset link would have first to insert an authentication code taken from the authentication API.

Entropy Sources
---------------
The main source of entropy for the platform is /dev/urandom.

In order to increase the entropy available on the system the system integrates the usage of the `Haveged <http://www.issihosts.com/haveged/>`_ daemon.

Web Application Security
========================
This section describes the Web Application Security functionalities implemented by following the `OWASP REST Security Cheat Sheet <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>`_.

Session management
------------------
The session implemenetation follows the `OWASP Session Management Cheat Sheet <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>`_ security guidelines.

The system assigns a Session to each authenticated user. The Session ID is 256bits long secret generated randomly by the backend. Each session expire accordingly to a timeout of 5 minutes. Session IDs are exchanged by the client with the backend by means of an header (X-Session) and do expire as soon that users close their browser or the tab running GlobaLeaks. Users could explicitly log out via a logout button or implicitly by closing the browser.

XSRF Prevention
---------------
Cookies are not used intentionally to minimize any possible XSRF attack.

Input Validation (backend)
--------------------------
The system adopts a whitelist based input validation approach. Each client request is checked against a set of regular expressions and only requests matching the expression are then processed.

As well a set of rules are applied to each request type to limit possible attacks. For example any request is limited to a payload of 1MB.

Input Validation (client)
-------------------------
The client implement strict validation of the rendered content by using the angular component `ngSanitize.$sanitize <http://docs.angularjs.org/api/ngSanitize.$sanitize>`_

Security related HTTP headers
-----------------------------
The system implements a large set of HTTP headers specifically crafted to improve the software security and achieves Security Headers [grade A](https://securityheaders.com/?q=https%3A%2F%2Ftry.globaleaks.org&followRedirects=on) and Mozilla Observatory [grade A+](https://observatory.mozilla.org/analyze/try.globaleaks.org)

Strict-Transport-Security
^^^^^^^^^^^^^^^^^^^^^^^^^
The system implements strict transport security by default.
::
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload

The preload feature is left optional to users and following the best practices is left disabled as default.

Content-Security-Policy
^^^^^^^^^^^^^^^^^^^^^^^
The backend implements the following Content Security Policy (CSP):
::
  Content-Security-Policy: default-src 'none'; script-src 'self'; connect-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self' data:; media-src 'self'; form-action 'self'; frame-ancestors 'none'; block-all-mixed-content

Feature-Policy
^^^^^^^^^^^^^^
The backend implements the following Feature-Policy header to limit the possible de-anonimization of the user by disabling dangerous browser features:
::
  Feature-Policy: camera 'none'; display-capture 'none'; document-domain 'none'; fullscreen 'none'; geolocation 'none'; microphone 'none; speaker 'none'

X-Frame-Options
^^^^^^^^^^^^^^^
The backend configure the X-Frame-Options header to prevent inclusion by means of Iframes in any site:
::
  X-Frame-Options', b'deny'

Referrer-Policy
^^^^^^^^^^^^^^^
Web-browsers usually attach referrers in their http headers as they browse links. The platform enforce a referrer policy to avoid this behaviour.
::

  Referrer-Policy: no-referrer

X-Content-Type-Options
^^^^^^^^^^^^^^^^^^^^^^
When setting up Content-Type for the specific output, we avoid the automatic mime detection logic of the browser by setting up the following header:
::

  X-Content-Type-Options: nosniff

X-XSS-Protection
^^^^^^^^^^^^^^^^
In addition in order to explicitly instruct browsers to enable XSS protections the Backend inject the following header:
::

  X-XSS-Protection: 1; mode=block

Crawlers Policy
^^^^^^^^^^^^^^^
For security reasons the backend instructs crawlers to avoid any caching and indexing of the application and uses the ``Robot.txt`` file to enable crawling only of the home page; indexing of the home page is in fact considered best practice in order to be able to widespread the information about the existance of the platform and ease access to possible whistleblowers.

The following is the ``Robots.txt`` configuration:
::
  User-agent: *
  Allow: /$
  Disallow: *

For high sensitive projects where the platform is inteded to remain ``hidden`` and commuicated to possible whistleblowers directly the platform could be as well configured to disable indexing completely.

The following is the ``HTTP Header`` injected in this case:
::
  X-Robots-Tag: noindex

Web Browser Privacy
-------------------
The Tor browser strives to remove as much identifiable information from requests as possible. It is still not perfect. For normal web browsers the situation is much more grave. The goals here are two: reduce the amount of application data and metadata stored on the a client’s machine, and reduce the amount of information about the client shared from client to backend.

Cache-control and other cache related headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The backend by default sends the following headers to instruct client’s browsers to not store resources in their cache.
As by section ``3. Storing Responses in Caches`` of `RFC 7234 <https://tools.ietf.org/html/rfc7234>`_ the platform uses the ``Cache-control`` HTTP header with the configuration ``no-store`` not instruct clients to store any entry to be used for caching; this settings make it not necessary to use any other headers like ``Pragma`` and ``Expires``.
::
  Cache-control: no-store

Anchor Tags and External URLs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In addition to the protecton offered by the header ``Referrer-Policy: no-referrer`` that prevents to pass the referrer while visiting the application sets the rel attribute nooopener to each of the external links. This protects from exectution of malicious content within the context of the application.
::
  <a href="url" rel="noopener">link title</a>

Cookies
-------
To prevent any potential abuse GlobaLeaks does not make use of any type of cookie.
Parsing of cookies is as well completely disabled to limit possible parsing attack surfaces.

Form Autocomplete OFF (client)
------------------------------
Form implemented by the platform make use of the HTML5 form attribute in order to instruct the browser to do not keep caching of the user data in order to predict and autocomplete forms on subsequent submissions.

This is achieved by setting `autocomplete=”false” <https://www.w3.org/TR/html5/forms.html=autofilling-form-controls:-the-autocomplete-attribute>`_ on the relevant forms or attributes.

Network Security
================
Tor
---
The software adopts `Tor <https://www.torproject.org/>`_ as default, prefferred and recommended connection encryption protocol for its security and each GlobaLeaks server by default implement an ``Onion Service v3``.
The use of ``Tor`` is recommended over HTTPS for its advanced properties of resistance to selective interception and censorship that would make it difficult for a third party to selectively capture or block tccess to the site to specific whistleblower or company department.

HTTPS
-----
The software enables easy setup of ``HTTPS`` offering both automatic setup via `Let'sEncrypt <https://letsencrypt.org/>`_ and manual setup. HTTPS is configured with ``TLS1.2+`` and its configuration is tuned to achieve `SSLLabs grade A+ <https://www.ssllabs.com/ssltest/analyze.html?d=try.globaleaks.org>`_.

Data Encryption
===============
The data, files, messages and metadata exchanged between whistleblowers and recipients is encrypted using the GlobaLeaks :doc:`EncryptionProtocol`.
In addition to this GlobaLeaks implements many other encryption components and the following is the set of the main libraries and their main usage:

* `Python-NaCL <https://github.com/pyca/pynacl>`_: is used for implementing data encryption
* `PyOpenSSL <https://github.com/pyca/pyopenssl>`_: is used for implementing HTTPS
* `Python-Cryptography <https://cryptography.io>`_: is used for implementing authentication
* `Python-GnuPG <http://pythonhosted.org/python-gnupg/index.html>`_: is used for encrypting email notifications

DoS Resiliency
==============
To avoid applicative and database denial of service, GlobaLeaks apply the following measures:

* It tries to limit the possibility of automating any operation by requiring human interaction (e.g. with the implementation of proof of work)
* It is written to limit the possibility of triggering CPU intensive routines by an external user (e.g. by implementing limits on queries and jobs execution time)
* It implements monitoring of each activity trying to implement detection of attacks and implement proactively security measures to prevent DoS (e.g. implementing slowdown on fast-operations)

Network Sandboxing
==================
GlobaLeaks integrates iptables by default and implements by a strict firewall rule that only allow inbound and outbound connections from 127.0.0.1 (where Tor is running with Tor Onion Service).

As well it automatically applies network sandboxing to all outbound communications that get automatically "torrified" (sent through Tor), being outbound TCP connections or DNS-query for name resolution.

Application Sandboxing
======================
GlobaLeaks integrates AppArmor by default and implements a strict sandboxing profile enabling the application to access only the strictly required files.
As well the application does run under a dedicated user and group "globaleaks" with reduced privileges.

Other Measures
==============
Encryption of Temporary Files
-----------------------------
Files being uploaded and temporarily stored on the disk during the upload process are encrypted with a temporary, symmetric AES-key in order to avoid writing any part of an unencrypted file's data chunk to disk. The encryption is done in "streaming" by using ``AES 128bit`` in ``CTR mode``. The key files are stored in memory and are unique for each file being uploaded.

Secure File Delete
------------------
Every file deleted by the application if overwritten before releasing the file space on the disk.

The overwrite routine is performed by a periodic scheduler and acts as following:

* A first overwrite writes 0 on the whole file;
* A second overwrite writes 1 on the whole file;
* A third overwrite writes random bytes on the whole file.

Secure Deletion of Database Entries
-----------------------------------
The platform enables the SQLite capability for secure deletion that automatically makes the database overwrite the data upon each delete query:
::
  PRAGMA secure_delete = ON
  PRAGMA auto_vacuum = FULL

Exception Logging and Redaction
-------------------------------
In order to quickly diagnose potential problems in the software when exceptions in clients are generated, they are automatically reported to the backend. The backend backend temporarily caches these exceptions and sends them to the backend administrator via email.

In order to prevent inadvertent information leaks the logs are run through filters that redact email addresses and uuids.

UUIDv4 Randomness
-----------------
Resources in the system like submissions and files are identified by a UUIDv4 in order to not be guessable by an external user and limit possible attacks.

TLS for SMTP Notification
-------------------------
All of the notifications are sent through SMTP over TLS encrypted channel by using SMTP/TLS or SMTPS, depending on the configuration.
