package org.dodgson.android.sleepandprofile

import android.animation.Animator
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.os.Bundle
import android.os.Debug
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.Switch
import androidx.appcompat.app.AppCompatActivity
import java.io.File
import java.util.concurrent.Executor
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean

class MainActivity : AppCompatActivity() {
    companion object {
        private val TAG : String = "MyActivity"
    }

    private lateinit var startButton: Button
    private lateinit var stopButton: Button
    private lateinit var methodTraceSwitch: Switch
    private lateinit var useSamplingSwitch: Switch
    private lateinit var useLockSwitch: Switch
    private val running : AtomicBoolean = AtomicBoolean(false)
    private val lockWorker : Executor = Executors.newSingleThreadExecutor { r -> Thread(r, "LockWorker") }
    private var animator: Animator? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        startButton = findViewById(R.id.button_start)
        startButton.setOnClickListener { start() }
        stopButton = findViewById(R.id.button_stop)
        stopButton.isEnabled = false
        stopButton.setOnClickListener { stop() }
        methodTraceSwitch = findViewById(R.id.switch_method_trace)
        useSamplingSwitch = findViewById(R.id.switch_sampling)
        useLockSwitch = findViewById(R.id.switch_lock)
    }

    override fun onStop() {
        super.onStop()
        stop()
    }

    private fun start() {
        startButton.isEnabled = false
        stopButton.isEnabled = true
        running.set(true)
        val wantsMethodTracing = methodTraceSwitch.isChecked
        val wantsSampling = useSamplingSwitch.isChecked
        val wantsLock = useLockSwitch.isChecked
        val tracePath = File(dataDir, "hello.trace")
        Thread({
            if (wantsMethodTracing) {
                Log.i(TAG, "Starting trace to " + tracePath.absolutePath)
                if (wantsSampling) {
                    Debug.startMethodTracingSampling(
                        tracePath.absolutePath,
                        16 * 1024 * 1024,
                        10 * 1000
                    )
                } else {
                    Debug.startMethodTracing(
                        tracePath.absolutePath,
                        16 * 1024 * 1024,
                        10 * 1000
                    )
                }
            }

            var i = 0
            while (running.get()) {
                Log.d(TAG, "Worker Running..." + (i++))
                if (wantsLock) {
                    lockOneSec()
                } else {
                    sleepOneSec()
                }
            }

            if (wantsMethodTracing)
                Debug.stopMethodTracing()
            Log.d(TAG, "Worker done.")
            startButton.post {
                startButton.isEnabled = true
                stopButton.isEnabled = false
            }
        }, "MyWorker").start()

        animator = ObjectAnimator.ofFloat(startButton, View.ALPHA, 1.0f, 0.0f).apply {
            repeatCount = ValueAnimator.INFINITE
            addListener(object : Animator.AnimatorListener {
                override fun onAnimationEnd(p0: Animator?) {
                    startButton.alpha = 1.0f
                }

                override fun onAnimationRepeat(p0: Animator?) {}
                override fun onAnimationCancel(p0: Animator?) {}
                override fun onAnimationStart(p0: Animator?) {}
            })
            start()
        }
    }

    private fun sleepOneSec() {
        Thread.sleep(1000)
    }

    private fun lockOneSec() {
        val lock = Object()
        lockWorker.execute {
            synchronized(lock) {
                Thread.sleep(1000)
            }
        }

        Thread.sleep(5) // wait for the worker to lock it.
        synchronized(lock) {
            Log.d(TAG, "Got the lock.")
        }
    }

    private fun stop() {
        running.set(false)
        animator?.end()
        animator = null
    }
}