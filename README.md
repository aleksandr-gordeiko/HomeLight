<h2>A module to set and maintain light rhythm in your house</h2>

<span style="color:#FFAA66"><i>The application is in alpha version</i></span>

<p>&ensp;It consists of a server, which interacts with your smart light bulb
and tells it what light brightness and temperature to set, according to
your schedule.<p>

<p>&nbsp;The schedule config is a <code>.json</code> file, where the "light
points" are written, e.g. my <code>schedule.json</code>:</p>

```json
{
  "6": {
    "brightness": 50,
    "temperature": 2700
  },
  "7": {
    "brightness": 160,
    "temperature": 3100
  },
  "8:30": {
    "brightness": 200,
    "temperature": 4000
  },
  "18": {
    "brightness": 140,
    "temperature": 3000
  },
  "21:30": {
    "brightness": 10,
    "temperature": 2700
  },
  "23": {
    "brightness": 0,
    "temperature": 0
  }
}
```

<p>&nbsp;The main config file is placed under <code>./config/config.json</code>
and necessarily contains:</p>

<ul>
<li><code>schedule_config_path</code>, which is path to
your schedule file</li>
<li><code>bulb_storage_path</code>, which is path to file where all known bulbs
stored, will be explained here next</li>
<li><code>broadcast_ip</code>, which the server sends message to for finding
light bulbs</li>
</ul>

<p>&nbsp;The optional parameters are:</p>

<ul>
<li><code>controller</code>, the type of bulb controller</li>
<li><code>update_period</code>, the polling period</li>
</ul>

<p>&nbsp;The server is able to store bulbs IP's it has once found, they are
automatically placed in a <code>.json</code>, which path is specified in
<code>config.json</code>. e.g. my <code>./data/bulbs.json</code>:</p>

```json
{
    "wiz": [
        "192.168.50.99"
    ]
}
```