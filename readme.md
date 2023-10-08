![QuantaVania](https://github.com/devilkiller-ag/QuantaVania/assets/43639341/ce51cd4b-bc14-45ee-bacd-b6d6d202548e)
<p align="center"><b>“Bridging the gap between quantum computation industry need and students in the field of quantum computing by means of an interactive quantum sandbox game.”</b></p>

<hr />
<p align="center"><b>Team Name: </b>SilentRaiders</p>
<p align="center"><b>Team Members: </b> <a href="https://www.linkedin.com/in/aniket-das-06829b141/" target="_blank">Aniket Das</a>, <a href="https://jaisarita.vercel.app/" target="_blank">Ashmit JaiSarita Gupta</a></p>
<hr />

<!-- ------------------------------------------------------------------------- -->

<h1>QuantaVania</h1>

<p>
 QuantaVania is an action-adventure 2D platformer game with the potential to evolve into an open-world sandbox game in which players can learn quantum computing from the ground up while playing, design their own game level, and share it with others in the quantum community via our web platform, and mine qubits, quantum gates and power-ups. 
</p>

<p>
 Our game will not only allow them to run the game on their local device but also on real quantum computers and simulators from various quantum computing providers like IBM Quantum, IONQ, Rigetti Computing, etc.
</p>

<p>
We intend to teach the players quantum computing as they go through the levels. We'll expose them to qubits in the first level, and then they'll have to find the X-Gate hiding behind any box or monster. As the levels progress, the player will discover new gates that he may use in the gun circuit. And, at the end of each level, we will introduce to the user each quantum algorithm, from basic to advanced, in the form of a game problem.
</p>

<!-- ------------------------------------------------------------------------- -->

<h2>Game Story</h2>
<p>
It is the year 2070, Quantum Computers are now mainstream. You are a Quantum software developer working on a VR game that fully immerses the user in a Quantum Computer game. While testing the game, you discover that you are unable to log out, the game glitches and you find yourself falling endlessly into an abyss, where your virtual avatar is stripped of its layers as it descends down the Dark Abyss with a faint greenish glow, and that you have become a small glowing cube of bits and qubits with the only thing left is your memory and soul encrypted in it.
</p>

<p>
But, determined to escape this perilous condition, you go into the neon dungeons, defeating the bots and collecting your avatar's lost data and quantum gates as you go. With each level you pass, you get one step closer to the actual world re-gaining your human avatar.
</p>

- Defeat enemies to collect qubits and quantum gates. Qubits are important for regaining health, and shield status, and defeating the enemies of the quantum world, quantum gates are required to upgrade weapons or solve challenges at each level.
- Every enemy has different states, configure the quantum circuit inside you (with the gates you collect) to match the enemy state and damage them.
- As you move towards a higher level, you have to solve interesting challenges based on quantum computing principles and algorithms.

Watch Gameplay on YouTube: https://youtu.be/hiG8MVEmIc8

<!-- ------------------------------------------------------------------------- -->

<h2>Controls</h2>

**Player Movement**
- **Left Arrow key:** Move the player to the left.
- **Right Arrow key:** Move the player to the right.
- **Spacebar:** Jump.

**Actions**
- **Right Mouse Click:** Shoot Qubit Bullet with the state as per the measurement result of the quantum circuit built by the player and also save this state as the player's state.
- **Left Mouse Click:** Save the player's state as per the measurement result of the quantum circuit built by the player.

**Building Quantum Circuit**
- **W, A, S, D Keys:** Move the "Circuit Cursor" in the Quantum Circuit to the place where you want to add a gate in the circuit.
- **Backspace Key:** Remove the gate present at the Circuit Cursor.
- **Delete Key:** Clear the Quantum Circuit, i.e., remove all gates from the Quantum Circuit.
- **X Key:** Add X Gate to the quantum circuit.
- **Y Key:** Add Y Gate to the quantum circuit.
- **Z Key:** Add Z Gate to the quantum circuit.
- **H Key:** Add H Gate to the quantum circuit.
- **C, R, E Keys:** Press **C Key** to convert the X, Y, Z, or H gates into CX, CY, CZ, and CH gates respectively, and then press **R Key** and **F Key** to the control to qubit above or below respectively.
- **Q and E Keys:** To convert X, Y, and Z into RX, RY, and RZ gates respectively. **Q Key** decreases the rotation angle by π/8 and **E Key** increases the rotation angle by π/8.

<!-- ------------------------------------------------------------------------- -->
<h2>Installation Instruction</h2>
To download and play QuantaVania, follow these steps:

<h3>Quick Instruction</h3>

```bash
git clone https://github.com/your-username/your-repo.git
cd QuantaVania
pip install -r requirements.txt
cd code
python main.py
```

<h3>Detailed Instruction</h3>

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Navigate to the game directory:

   ```bash
   cd QuantaVania
   ```
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv qvenv
    ```
4. Activate the virtual environment:
    - On Windows:
      ```bash
      qvenv\Scripts\activate
      ```
    - On macOS and Linux:
      ```bash
      source qvenv/bin/activate
      ```
5. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
6. Navigate to the game code directory:
   ```bash
   cd code
   ```
7. Run main.py to play the QuantaVania Game:
   ```bash
   python main.py
   ```
8. Additionally Run qubo_minigame.py to play the QUBO Challenge Level
   ```bash
   python qubo_minigame.py
   ```
<!-- ------------------------------------------------------------------------- -->
<hr />

<h1>Problem we are trying to solve</h1>

<p align="center"><b>“The gap between quantum computation industry needs and students in the field of quantum computing.”</b></p>

<p>
The gap between the quantum computation industry's needs and students in the field of quantum computing is significant. According to McKinsey & Company, there is only one qualified quantum candidate available for every three quantum job openings. By 2025, they predict that less than 50 percent of quantum computing jobs will be filled unless significant interventions occur.
</p>

<p>
There are a number of factors contributing to this gap. One of the main factors is that students find it difficult to get started in this field due to a lack of educational resources focusing on audiences with no experience. Usually, undergraduate students with no experience in reading documentation and research papers find it difficult to understand the concepts of quantum computing through them.
</p>

<p>
The quantum computing industry is growing rapidly, and there is a strong demand for qualified workers. Companies are looking for people with a variety of skills, including quantum computing theory, quantum algorithms, and quantum software development. Bridging this gap is crucial to unlocking the true potential of quantum technologies.
</p>

<!-- ------------------------------------------------------------------------- -->

<h2>Our Solution</h2>

<p align="center"><b>“Bridging the gap between quantum computation industry need and students in the field of quantum computing by means of an interactive quantum sandbox game.”</b></p>

<p>
We are trying to bridge the gap between the quantum computation industry needs and students in the field of quantum computing by means of a quantum sandbox game that allows the player to learn the concepts of quantum computing from basics to advanced algorithms through puzzles and mining.
</p>

<!-- ------------------------------------------------------------------------- -->

<h2>How our game is different from regular platformer games</h2>

- The behavior of players and enemies works through the control of the Quantum Circuit. 
- Each Level is designed to teach the player the concepts of quantum computing and algorithms from basics to advance by means of a topic introduction at the beginning of the level and then apply that topic throughout the level and in the Mini-Challenge at the end of each level which has to be solved by the player to unlock the next level.
- Players can run the game on different simulators and real quantum computing devices by various providers.
- Players can design, save, and play their own custom levels made by them. They can also share these levels with their friends through our web platform and quantum computing community.

<!-- ------------------------------------------------------------------------- -->

<h2>Current Stage and Future Plans</h2>

<p>
As of now, the game has been designed as a submission to the Quantum Games Hackathon. We have used Python, PyGame, and Qiskit as the backend for the game. And the levels are limited to 3 pre-designed levels, and a custom level creator for the player to create as many levels as they want and how they want.
</p>

<p>
 We want our game to have endless creative possibilities, similar to games like Terraria and Minecraft. What makes these games great is the freedom of a sandbox and a choose-your-own-adventure type of loose storyline. We plan to create an open-world sandbox-like game where players can mine to collect qubits, quantum gates, and power-ups. We will also change our tech stack from Pygame to C# or C++. Initially, we will be targeting the PC platform.
</p>

<!-- ------------------------------------------------------------------------- -->

<h2>Business Plans and Game Monetisation</h2>

<p>The ideas that we currently have for monetizing our games are:</p>

- Subscription-based Special Level Themes and skins of players and enemies.
- For the free tier, he can run the Quantum Circuit by only using the Qiskit Aer Simulator. He can compute times from various quantum computing cloud providers individually.
- Special tier of weapons, powers, and theme levels for subscribed players.
- Players can buy different player avatars and gun skins independently from the subscription.

<!-- ------------------------------------------------------------------------- -->

<h2>Startup Plan</h2>

<p>
We plan to convert our project into a marketable product and start a startup. We will shift our tech stack to C# for procedural level generation and create a game suitable for beginners in quantum computing as well as someone who is advanced in this field and wants to enjoy a professional game based on QC. We will collaborate with various Quantum Computing Cloud Providers to make their free as well as paid simulators & devices available for our players.
</p>

<!-- ------------------------------------------------------------------------- -->

<h2>Competition</h2>

<p>
The first quantum software game was Cat-Box-Scissors, developed in 2017 by IBM researcher James Wootton. Since then many quantum games like Quantum Oddysey and Hello Quantum have been published based on one quantum concept or another. Most of these quantum games are just puzzle-based or only cover some specific concept of quantum computation.
</p>

<p>
QuantaVania’s aim is to teach players quantum computation to the player in a sequential way from basics to advance not only through puzzles but through platformer and sandbox-like experiences. We allow players to create and share their own custom level through our web community platform bringing a shared and collaborative learning experience.
</p>
