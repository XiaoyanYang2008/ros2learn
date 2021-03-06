### Get the code
```
cd ~ && git clone -b dashing https://github.com/XiaoyanYang2008/ros2learn.git
cd ros2learn
git submodule update --init --recursive
```
#### Useful info
- Pull all the new commits: `git pull --recurse-submodules && git submodule update --recursive --remote`
- Quick reference for submodules ([1](http://www.vogella.com/tutorials/GitSubmodules/article.html), [2](https://chrisjean.com/git-submodules-adding-using-removing-and-updating/), [3](https://git-scm.com/book/en/v2/Git-Tools-Submodules))

### Install each module
This repository contains various modules that need to be installed independently:

- **gym-gazebo2**: is a toolkit for developing and comparing reinforcement learning algorithms using ROS 2 and Gazebo. Follow the [instructions](https://github.com/AcutronicRobotics/gym-gazebo2/blob/dashing/INSTALL.md) to install it. During "Compile the workspace" step, may need to 
  ```sh
  pip3 install empy catkin-pkg lark-parser sip==4.19.8
  ```
  Unzip sip.zip to python3 site-packages/dist-packages folder if "ModuleNotFoundError: No module named 'sipconfig' " during python_orocos_kdl colcon build.
  Unzip PyKDL.so.zip to ros2_mara_ws/install/lib/python3/dist-packages if error "PyKDL.so: undefined symbol: PyString_FromString" encountered during model training, e.g. python3 train_ppo2_mlp.py

- **baselines**: is a slightly adapted version of OpenAI's baselines repository to address robotics use cases with a set of high-quality implementations of reinforcement learning algorithms. To install it:

  ```sh
  cd ~/ros2learn/algorithms/baselines
  pip3 install -e .
  ```

### Dependent tools

```bash
pip3 install matplotlib
sudo apt install python3-tk
```
