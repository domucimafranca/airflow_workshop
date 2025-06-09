# Running the Backend

## Instantiating in Docker

Go to `backend/` and instantiate the containers in `docker-compose.yml`. 

The docker-compose file sets up MariaDB, phpMyAdmin, and MinIO.

Modify the credentials as needed.


## Set up loyalty database
Generate `transactions.csv` using `utils/data_generator.py`.

Make a `loyalty` database.  This can be done from phpMyAdmin.

Import `transactions.csv` to `transactions` table of `loyalty` database.  
This can be done from phpMyAdmin.

## MariaDB access

Create additional users as needed. Give them access to 

```
CREATE USER 'group1';
GRANT ALL PRIVILEGES ON loyalty.* TO 'group1'@'%';
```

Test access to the database from command line MySQL client, ideally from the same
machine you will be running Airflow on. You may need to install the mysql client.

`mysql -u group1 -h 192.168.88.98 -p`

## Set up MinIO access

On MinIO web UI, go to Access Keys. Make a new Access Key.  Access Key and Secret Key
are the important parameters. You can download this as a file.

Install s3cmd on your machine. 

`sudo apt install s3cmd`

Configure s3cmd.

`s3cmd --configure`

Sample session:

```
Enter new values or accept defaults in brackets with Enter.
Refer to user manual for detailed description of all options.

Access key and Secret key are your identifiers for Amazon S3. Leave them empty for using the env variables.
Access Key [SpRbosNBt7BF96HLsN5G]: TIOzEVsIrDQKuvUgEv6c
Secret Key [v1VUR1H3R0p3hjTNFVZQRVqlcJdNIugTERsRiptE]: gtIJXDHAyUwNCQRbihgEszUiacrkuCmgKIlEsX31
Default Region [US]: 

Use "s3.amazonaws.com" for S3 Endpoint and not modify it to the target Amazon S3.
S3 Endpoint [192.168.88.98:9000]: 

Use "%(bucket)s.s3.amazonaws.com" to the target Amazon S3. "%(bucket)s" and "%(location)s" vars can be used
if the target S3 system supports dns based buckets.
DNS-style bucket+hostname:port template for accessing a bucket [192.168.88.98:9000]: 

Encryption password is used to protect your files from reading
by unauthorized persons while in transfer to S3
Encryption password: 
Path to GPG program [/usr/bin/gpg]: 

When using secure HTTPS protocol all communication with Amazon S3
servers is protected from 3rd party eavesdropping. This method is
slower than plain HTTP, and can only be proxied with Python 2.7 or newer
Use HTTPS protocol [No]: 

On some networks all internet access must go through a HTTP proxy.
Try setting it here if you can't connect to S3 directly
HTTP Proxy server name: 

New settings:
  Access Key: TIOzEVsIrDQKuvUgEv6c
  Secret Key: gtIJXDHAyUwNCQRbihgEszUiacrkuCmgKIlEsX31
  Default Region: US
  S3 Endpoint: 192.168.88.98:9000
  DNS-style bucket+hostname:port template for accessing a bucket: 192.168.88.98:9000
  Encryption password: 
  Path to GPG program: /usr/bin/gpg
  Use HTTPS protocol: False
  HTTP Proxy server name: 
  HTTP Proxy server port: 0

Test access with supplied credentials? [Y/n] 
Please wait, attempting to list all buckets...
Success. Your access key and secret key worked fine :-)

Now verifying that encryption works...
Not configured. Never mind.

Save settings? [y/N] Y
Configuration saved to '/home/dom/.s3cfg'
```

## Test MinIO access

```
s3cmd ls
s3cmd mb s3://group-1
s3cmd ls
s3cmd put myfile.txt s3://group-1
s3cmd ls s3://group-1
```
