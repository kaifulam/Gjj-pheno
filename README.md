## Particle identification and Machine Learning - Single b tagging

![Standard Model](https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Standard_Model_of_Elementary_Particles.svg/300px-Standard_Model_of_Elementary_Particles.svg.png)

Particle identification and Machine Learning... If you found this page, I'm sure you've at least watched a few youtube videos about these two things! You're a certified geek!

This project focused on b-tagging, the identification of bottom quarks in a particle accelerator detector. Here is a link to my paper ["b tagging using neural network"](https://drive.google.com/file/d/0B3qwNGluXsHSQ05XV2wzQXRraTA). 

Before you dig into my codes, below are some good intuition refreshers...

**b-tagging** - [SLAC public lecture](https://youtu.be/Sd7T23h334g), [The Standard Model by DrPhysicsA](https://youtu.be/d1zaw-KZX1o)

**Neural Network in Machine Learning** - [DeepLearning.TV series](https://youtu.be/b99UVkWzYTQ), [Andrew Ng on Coursera](https://www.coursera.org/learn/machine-learning)

![Large Hadron Collider](http://stanford.edu/group/stanford_atlas/pictures/collision/LHC.jpg)

The [7 detectors](https://home.cern/about/experiments) along the [Large Hadron Collider (LHC)](https://home.cern/topics/large-hadron-collider) are like big data generators. The LHC guide particles to smash against each other head on, and the detectors record all the bits and pieces that come out of it.

There're many smart people in CERN. (duh..) Some of them write algorithms to reconstruct trajectories of particles inside the detector. This is like tracing a [multiple head missile](https://en.wikipedia.org/wiki/Multiple_independently_targetable_reentry_vehicle#/media/File:Minuteman_III_MIRV_path.svg) backwards to the origin. The goal here is to identify the original particle (actually observed as [Jets](https://en.wikipedia.org/wiki/Jet_(particle_physics))) that creates all these mess in the detector based on a collection of trajectory variables.

This is where neural network comes in! We train the neural network by feeding in the variables of each jet, and give it the correct answer (say.. jet of a bottom quark). After seeing say.. 10 million examples, we see that the neural network model learn to identify particles, and it performs better than if we were to identify particles using each variable alone.

This is a follow on study of [this](https://arxiv.org/pdf/1607.08633.pdf) paper by [Dan Guest](https://github.com/dguest/delphes-rave/wiki/Output-Format)

Instructions to run the codes is [here](https://drive.google.com/file/d/0B3qwNGluXsHSUW9fdTNDRHh0LW8/view?usp=sharing)

Expert Level variables explained [here](https://drive.google.com/file/d/0B3qwNGluXsHSUW9fdTNDRHh0LW8/view?usp=sharing)
