### Result

The best result I managed to obtain was solving the taks in 664 episodes. The plot below shows how the scores as the episodes elapsed.

![scores X episodes](https://github.com/thiagomarzagao/p1_navigation/blob/master/Figure_1.png)

### The DQN model

To achieve that result I used an adapted version of the [Deep Q-Learning](https://www.nature.com/articles/nature14236) model. The DQN is a neural network that approximates the optimal action-value function *Q* of conventional reinforcement learning algorithms. This approximation is necessary when the number of possible states is large (here it's infinite, as each of the 37 state dimensions is continuous). Hence instead of updating *Q(s,a)* at every iteration, as we would do in a conventional RL algorithm, here we update *Q(s,a,theta_i)*, where *theta_i* are the neural network's weights at iteration *i*.

The important aspects of the DQN model are not so much its architectural details but two separate innovations: experience replay and target network. "Experience replay" means sampling randomly from a buffer of past experiences, each being a tuple of states, actions, and rewards: (s_t, a_t, r_t, s_t+1). By sampling randomly in the training stage we fix the problem of correlated states, which before the DQN model had limited the application of deep learning to reinforcement learning. "Target network" is a separate neural network with the same architecture of the main netural network but only updated every couple of iterations. The target network replaces the main network when we pick the action. That weakens the correlation between action-values and targets.

### Adaptations

I used experience replay just as described in the original DQN paper (with a buffer size of 100k). I changed the target network though. Instead of outright cloning the main network I used a soft update, as suggested in the nanodegree lessons, to make the target network closer to the main network. I set the soft updates to happen every four iterations.

I also made changes to the architecture of the DQN model. The original DQN model consists of three convolutional layers followed by two fully connected layers. But he original DQN model uses images as inputs, which is not the case here (our 37-dimensional state represents the agent's velocity, position, etc, instead of pixels). Hence I removed the convolutional layers. Also, here our action space has only four dimensions (forward, backward, left, right), so that's the dimensionality of our output layer (as opposed to the 18 combinations of joystick direction and button of the original DQN model, which was meant to learn how to play Atari games).

More importantly, here I used only one hidden layer. As Jeff Heaton argues in his book [Introduction to Neural Networks for Java](https://dl.acm.org/citation.cfm?id=1502373), "*Problems that require two hidden layers are rarely encountered. However, neural networks with two hidden layers can represent functions with any kind of shape. There is currently no theoretical reason to use neural networks with any more than two hidden layers. In fact, for many practical problems, there is no reason to use any more than one hidden layer.*"

I set the number of neurons of the hidden layer at 24, following the rule of thumb that the size of a hidden layer should be somewhere between that of the input layer (37) and that of the output layer (4), and ideally a power of 2 (to facilitate computation). I tried other values (16, 32, 64, 128) but found little effect on the result. The activation function is RELU.

As for the hyperparameters, I set gamma (the discount factor) at 0.99, tau (used in the soft update) at 0.001, and the learning rate at 0.0005. I tried tweaking these values but that resulted in no improvement.

### Ideas for future improvements

In the future it might be worth it to try the Double-DQN algorithm with prioritized experience replay, as suggested in the nanodegree lesson. However, given that we can obtain a reasonable result with only one hidden layer of 24 neurons, a more enticing approach might be ditching neural networks entirely for this task and trying multinomial logit instead. A multinomial logit model, even if it performed slightly worse, would have the advantage of being interpretable - we could inspect the estimated coefficients to try to understand what's going on "under the hood" (why a state with such and such characteristics leads to such and such actions, etc).

An interesting extension would be to take the task to the phyisical world. I have a set of LEGO Mindstorms and a while ago I wrote a [module](https://github.com/thiagomarzagao/ev3py) that lets us program it using Python. It might be interesting to see what happens when we attach a camera to it, adjust the state dimensions, find a way to randomly (re-)throw a bunch of fake bananas at every iteration, etc. It would probably help me have a better idea of the challenges of applying reinforcement learning to robotics in the real world.
