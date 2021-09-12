
# Stackoverflow Crawler

A web crawler which crawls the **Stack Overflow** website. (Questions and Answers / Q&A)

[![stackoverflow](logo.png)](https://stackoverflow.com/)

### Try API

- https://stackoverflow.com/questions/tagged/c
- https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=stackoverflow&pagesize=100
- https://api.stackexchange.com/2.2/questions/1163244?order=desc&sort=activity&site=askubuntu
- https://api.stackexchange.com/2.2/questions/1160229/answers?order=desc&sort=activity&site=askubuntu
- https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&site=askubuntu&pagesize=100
- https://api.stackexchange.com/docs/questions

### Stack Exchange API

- https://api.stackexchange.com/
- https://api.stackexchange.com/docs
- https://stackapps.com/questions/7/how-to-list-your-application-library-wrapper-script-here
- http://stackapps.com/apps/oauth/register
- https://api.stackexchange.com/docs/throttle
- https://api.stackexchange.com/docs/authentication
- https://api.stackexchange.com/docs/write

-------

It's same as a fork and depends on some other projects on the GitHub:

- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://pypi.org/project/bs4/
- https://pypi.org/project/beautifulsoup4/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/#get-text
- https://github.com/topics/stackoverflow-crawler
- https://github.com/rjstyles/StackOverflow-Crawler
- https://github.com/topics/stackoverfolw-website
- ...

I did not remember that at now.

---------

## Testing

```
$ python3 craw.py
crawling page 1: https://stackoverflow.com/questions/tagged/c%2b%2b?sort=votes&page=1&pageSize=15
------------------------------
Why is processing a sorted array faster than processing an unsorted array?
<div class="post-text" itemprop="text">
<p>Here is a piece of C++ code that shows some very peculiar behavior. For some strange reason, sorting the data miraculously makes the code almost six times faster:</p>
<pre class="lang-cpp prettyprint-override"><code>#include &lt;algorithm&gt;
#include &lt;ctime&gt;
#include &lt;iostream&gt;

int main()
{
	// Generate data
	const unsigned arraySize = 32768;
	int data[arraySize];

	for (unsigned c = 0; c &lt; arraySize; ++c)
		data[c] = std::rand() % 256;


	// !!! With this, the next loop runs faster.
	std::sort(data, data + arraySize);


	// Test
	clock_t start = clock();
	long long sum = 0;

	for (unsigned i = 0; i &lt; 100000; ++i)
	{
		// Primary loop
		for (unsigned c = 0; c &lt; arraySize; ++c)
		{
			if (data[c] &gt;= 128)
				sum += data[c];
		}
	}

	double elapsedTime = static_cast&lt;double&gt;(clock() - start) / CLOCKS_PER_SEC;

	std::cout &lt;&lt; elapsedTime &lt;&lt; std::endl;
	std::cout &lt;&lt; "sum = " &lt;&lt; sum &lt;&lt; std::endl;
}
</code></pre>
<ul>
<li>Without <code>std::sort(data, data + arraySize);</code>, the code runs in 11.54 seconds.</li>
<li>With the sorted data, the code runs in 1.93 seconds.</li>
</ul>
<hr/>
<p>Initially I thought this might be just a language or compiler anomaly, so I tried Java:</p>
<pre class="lang-java prettyprint-override"><code>import java.util.Arrays;
import java.util.Random;

public class Main
{
	public static void main(String[] args)
	{
		// Generate data
		int arraySize = 32768;
		int data[] = new int[arraySize];

		Random rnd = new Random(0);
		for (int c = 0; c &lt; arraySize; ++c)
			data[c] = rnd.nextInt() % 256;


		// !!! With this, the next loop runs faster
		Arrays.sort(data);


		// Test
		long start = System.nanoTime();
		long sum = 0;

		for (int i = 0; i &lt; 100000; ++i)
		{
			// Primary loop
			for (int c = 0; c &lt; arraySize; ++c)
			{
				if (data[c] &gt;= 128)
					sum += data[c];
			}
		}

		System.out.println((System.nanoTime() - start) / 1000000000.0);
		System.out.println("sum = " + sum);
	}
}
</code></pre>
<p>with a similar but less extreme result.</p>
<hr/>
<p>My first thought was that sorting brings the data into the cache, but then I thought how silly that was because the array was just generated.</p>
<ul>
<li>What is going on?</li>
<li>Why is processing a sorted array faster than processing an unsorted array? The code is summing up some independent terms, so the order should not matter.</li>
</ul>
</div>
List of answers:


===>
Why is processing a sorted array faster than processing an unsorted array?

You are a victim of branch prediction fail.

What is Branch Prediction?
Consider a railroad junction:

Image by Mecanismo, via Wikimedia Commons. Used under the CC-By-SA 3.0 license.
Now for the sake of argument, suppose this is back in the 1800s - before long distance or radio communication.
You are the operator of a junction and you hear a train coming. You have no idea which way it is supposed to go. You stop the train to ask the driver which direction they want. And then you set the switch appropriately.
Trains are heavy and have a lot of inertia. So they take forever to start up and slow down.
Is there a better way? You guess which direction the train will go!

If you guessed right, it continues on.
If you guessed wrong, the captain will stop, back up, and yell at you to flip the switch. Then it can restart down the other path.

If you guess right every time, the train will never have to stop.
If you guess wrong too often, the train will spend a lot of time stopping, backing up, and restarting.

Consider an if-statement: At the processor level, it is a branch instruction:

You are a processor and you see a branch. You have no idea which way it will go. What do you do? You halt execution and wait until the previous instructions are complete. Then you continue down the correct path.
Modern processors are complicated and have long pipelines. So they take forever to "warm up" and "slow down".
Is there a better way? You guess which direction the branch will go!

If you guessed right, you continue executing.
If you guessed wrong, you need to flush the pipeline and roll back to the branch. Then you can restart down the other path.

If you guess right every time, the execution will never have to stop.
If you guess wrong too often, you spend a lot of time stalling, rolling back, and restarting.

This is branch prediction. I admit it's not the best analogy since the train could just signal the direction with a flag. But in computers, the processor doesn't know which direction a branch will go until the last moment.
So how would you strategically guess to minimize the number of times that the train must back up and go down the other path? You look at the past history! If the train goes left 99% of the time, then you guess left. If it alternates, then you alternate your guesses. If it goes one way every three times, you guess the same...
In other words, you try to identify a pattern and follow it. This is more or less how branch predictors work.
Most applications have well-behaved branches. So modern branch predictors will typically achieve >90% hit rates. But when faced with unpredictable branches with no recognizable patterns, branch predictors are virtually useless.
Further reading: "Branch predictor" article on Wikipedia.

As hinted from above, the culprit is this if-statement:
if (data[c] >= 128)
	sum += data[c];

Notice that the data is evenly distributed between 0 and 255. When the data is sorted, roughly the first half of the iterations will not enter the if-statement. After that, they will all enter the if-statement.
This is very friendly to the branch predictor since the branch consecutively goes the same direction many times. Even a simple saturating counter will correctly predict the branch except for the few iterations after it switches direction.
Quick visualization:
T = branch taken
N = branch not taken

data[] = 0, 1, 2, 3, 4, ... 126, 127, 128, 129, 130, ... 250, 251, 252, ...
branch = N  N  N  N  N  ...   N    N    T    T    T  ...   T    T    T  ...

	   = NNNNNNNNNNNN ... NNNNNNNTTTTTTTTT ... TTTTTTTTTT  (easy to predict)

However, when the data is completely random, the branch predictor is rendered useless, because it can't predict random data. Thus there will probably be around 50% misprediction (no better than random guessing).
data[] = 226, 185, 125, 158, 198, 144, 217, 79, 202, 118,  14, 150, 177, 182, 133, ...
branch =   T,   T,   N,   T,   T,   T,   T,  N,   T,   N,   N,   T,   T,   T,   N  ...

	   = TTNTTTTNTNNTTTN ...   (completely random - hard to predict)


So what can be done?
If the compiler isn't able to optimize the branch into a conditional move, you can try some hacks if you are willing to sacrifice readability for performance.
Replace:
if (data[c] >= 128)
	sum += data[c];

with:
int t = (data[c] - 128) >> 31;