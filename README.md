<a id="readme-top"></a>
<br />
<div align="center">
  </a>

<h3 align="center">Smart Public Transport Advisor</h3>

  <p align="center">
    A flexible route optimizer for planning your journeys!
    <br />
    <a href="https://github.com/anson20070818-dot/COMP1110E08"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/anson20070818-dot/COMP1110E08">View Demo</a>
    &middot;
    <a href="https://github.com/anson20070818-dot/COMP1110E08/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/anson20070818-dot/COMP1110E08/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-this-project">About This Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-and-execution">Installation and Execution</a></li>
        <li><a href="#file-description">File Description</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
      <li><a href="#guide">Guide</a></li>
        <li><a href="#network-format">Network Format</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


<!-- ABOUT THIS PROJECT -->
## About This Project

No matter where you live, choosing a public transport route is a common daily-life problem for students, workers, and other commuters. A travel decision often involves balancing several factors, such as travel time, cost, number of transfers, and convenience.

Although existing apps like Google Maps provide useful route information, they may not always present options in a way that fits different user priorities equally well. Some tools focus more on speed, some provide only partial fare information, and some are limited to specific transport modes.

Our project aims to model this commuting problem as a simple computing problem. We've built a Smart Public Transport Advisor that represents a transport network using stops and segments, generating possible journeys between origin and destination. Our system allows users to compare routes based on different preferences, such as cheapness, speed, or fewest transfers.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Please read the following to understand how to use our transport advisor.

### Prerequisites

Our project is built entirely with Python! So you'll need the following
- Python: Version 3.9 or higher installed
- Pip: Comes with Python

### Installation and Execution

1. Clone the repo or simply download and extract the .zip
   ```sh
   git clone https://github.com/anson20070818-dot/COMP1110E08.git
   cd COMP1110E08
   ```
2. For Windows, install the dependencies using
   ```sh
   pip install -r requirements.txt
   ```
   For Linux/macOS, install the dependencies using
   ```sh
   pip3 install -r requirements.txt
   ```
3. For Windows, run the program from root using
   ```sh
   python -m transport_advisor
   ```
   For Linux/macOS, use the following instead
   ```sh
   python3 -m transport_advisor
   ```

If you haven't followed steps 2 and 3 precisely, you may receive a warning message

### File Description

Below details the purpose of each folder & file

`data`: Contains example networks in correct format for view and usage

`transport_advisor`: Contains all program files
- `__init__.py`: Marks transport_advisor as a regular Python package
- `__main__.py`: Entry point of the system, containing the menu interface and allowing you to utilize all the features of our advisor
- `load_network.py`: Handles the loading of your network .csv file
- `network_analysis.py`: Contains useful functions to retrieve network information
- `find_path.py`: Handles the generation of candidate routes within the network
- `filter_sort.py`: Handles the filtering and sorting of routes according to preference

`requirements.txt`: Contains the list of required Python dependencies

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

After running the program by following the execution steps, you'll be greeted with the menu and a list of commands. To execute a command, press the corresponding number key shown on the left. There is no need to press enter.

![Menu](https://dl.dropboxusercontent.com/scl/fi/92ys356t0qxeircdsohwl/Menu.png?rlkey=kw4p2e7olhti6io9twy3djdvj&st=gd4jzsqm?raw=1 "Menu")
There are 4 commands you can run:
1. Generate Journeys: Begins generation of routes, you cannot run this until you've loaded a network
2. Load Network: Loads a network stored inside the `data` folder
3. View Network Summary: Shows network information, such as all stop names and total number of segments
4. Quit Program: Exits the program, run this once you're done

### Guide
The following is a quick step-by-step guide on using the system!

First, we must load the network using `Load Network`. You'll be prompted to input the name of the network file, make sure to type the full exact name with case-sensitivity.

_Tip: If the file's name is network.csv you can simply press enter_

![File Name Input](https://dl.dropboxusercontent.com/scl/fi/ao6156s846qh7d5pxul0k/FileNameInput.png?rlkey=4j8ro64dqds380ck4o7hfdzh0&st=sersi48c?raw=1 "File Name Input")

If an error occurs, ensure that the file is placed inside the `data` folder, and that the network follows the correct format (See <a href="#network-format">Network Format</a>)

Then, you can use `View Network Summary` to see all stop names in case you forget, and other helpful information.

![Network Summary](https://dl.dropboxusercontent.com/scl/fi/0pzpgs31nb5wimtp1ns3a/Summary.png?rlkey=b3p2re20t4vm7jvosewwtqg26&st=kfmtd583?raw=1 "Network Summary")

Now, you're all set to generate routes! Run `Generate Journeys` and input the names of the desired origin and destination stops exactly.

![Generate Journeys](https://dl.dropboxusercontent.com/scl/fi/f5qoyjxnde6rzl3vy4bkd/Generate-Journeys.png?rlkey=9yale8gp9yc3w6x4js5gifsvf&st=bcoghs81?raw=1 "Generate Journeys")

Run `View Top Journeys` and select your preferences, you can select to not have a 2nd preference. Then, you can filter out any transport mode(s) and select `Finish Filter Input` once you're done.

Your routes will then be processed immediately and the top 3 routes according to your preferences will be displayed in ascending order!

![Results](https://dl.dropboxusercontent.com/scl/fi/ir1iy3ermhyxrqt8xsl9p/Results.png?rlkey=d7msel3ibqj30xmvwknhvpphw&st=u4lewmeg?raw=1 "Results")

You can keep running `View Top Journeys` and select different preferences or filters. Once you're done or you want to load a different network, run `Return to Start` to go back to the main menu screen.

_For further demonstation of using our advisor system, please refer to this [video demo](https://example.com)!_

### Network Format
Your network file must be in .csv format for it to load properly. Each record in the file represents a segment (i.e. a way of going from `From_Stop` to `To_Stop` using the transport `Mode`).

Please follow the format below strictly:
| From_Stop | To_Stop | Duration | Cost | Mode |
| -------- | -------- | -------- | -------- | -------- |
| (Stop Name) | (Stop Name) | (Number ≥ 0) | (Number ≥ 0) | (Transport Name) |

Example of a valid network (Included in the `data` folder, this is only a snippet):
```
From_Stop,To_Stop,Duration,Cost,Mode
Stop 1,Stop 5,4,8.0,Metro
Stop 5,Stop 10,4,7.0,Metro
Stop 10,Stop 15,4,8.0,Metro
Stop 1,Stop 2,6,2.0,Bus
Stop 2,Stop 3,5,1.0,Bus
Stop 3,Stop 4,4,1.0,Bus
Stop 4,Stop 8,7,2.0,Bus
Stop 8,Stop 12,6,1.0,Bus
Stop 12,Stop 13,4,1.0,Walking
```

You can enter any name for the stop and transport mode, note that any difference between names will be treated as separate. Even if a line(s) contains invalid data, the network can be loaded without that particular line(s) as long as there is 1 valid line.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the Apache-2.0 license. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
