"""
with SimpleTimer("optional message") as timer:
    # do thing1
    timer.track("thing1")
    # do thing2
    timer.track("thing2")

    # Get timing summary before exiting context
    timing_data = timer.get_timing_summary()

# timing_data = [
#     {"step": "thing1", "duration_ms": 223},
#     {"step": "thing2", "duration_ms": 132},
#     {"step": "total", "duration_ms": 355}
# ]

# when exiting, it should just print out:
Timer: [thing1: 223ms], [thing2: 132ms], TOTAL: 355ms
"""

import time
import logging
from typing import List, Tuple, Optional, TypedDict

logger = logging.getLogger(__name__)


class TimingStep(TypedDict):
    """Timing information for a single step."""
    step: str
    duration_ms: int


class SimpleTimer:
    def __init__(self, message: Optional[str] = None):
        self._message = message
        self._start_time: float = 0.0
        self._end_time: Optional[float] = None
        self._tracks: List[Tuple[str, float]] = []
        self._last_track_time: float = 0.0

    @property
    def duration(self) -> float:
        """Returns the elapsed time in seconds since the timer started."""
        if self._end_time:
            return self._end_time - self._start_time
        if self._start_time > 0:
            return time.perf_counter() - self._start_time
        return 0.0

    def get_timing_summary(self) -> List[TimingStep]:
        """Returns timing data as a list of TimingStep dicts preserving execution order."""
        result: List[TimingStep] = []
        for name, duration in self._tracks:
            result.append({
                "step": name,
                "duration_ms": round(duration * 1000)
            })

        total_duration = self.duration
        result.append({
            "step": "total",
            "duration_ms": round(total_duration * 1000)
        })

        return result

    def __enter__(self):
        if self._message:
            logger.info(self._message)
        self._start_time = time.perf_counter()
        self._last_track_time = self._start_time
        self._end_time = None
        return self

    def track(self, name: str):
        now = time.perf_counter()
        duration = now - self._last_track_time
        self._tracks.append((name, duration))
        self._last_track_time = now

    def track_and_show_duration(self, name: str):
        now = time.perf_counter()
        duration = now - self._last_track_time
        self._tracks.append((name, duration))

        if len(self._tracks) > 1:
            prev_name = self._tracks[-2][0]
            logger.info(f"Duration: {duration * 1000:.0f}ms - [{prev_name} -- {name}]")
        else:
            logger.info(f"Duration: {duration * 1000:.0f}ms - [start -- {name}]")

        self._last_track_time = now

    def merge_timing_summary(self, timing_summary: List[TimingStep], exclude_total: bool = True) -> None:
        """Merge timing steps from another timer's summary into this timer.

        Args:
            timing_summary: List of TimingStep dicts from another timer's get_timing_summary()
            exclude_total: If True, excludes the 'total' step from the merge (default True)

        Usage:
            with SimpleTimer("main") as main_timer:
                main_timer.track("step1")

                # Call another operation that returns timing
                result, sub_timing = await some_operation()

                # Merge sub-operation timing into main timer
                main_timer.merge_timing_summary(sub_timing)

                main_timer.track("step2")

                # get_timing_summary() now includes all merged steps
        """
        for timing_step in timing_summary:
            if exclude_total and timing_step['step'] == 'total':
                continue
            # Convert ms back to seconds and add to tracks
            duration_seconds = timing_step['duration_ms'] / 1000.0
            self._tracks.append((timing_step['step'], duration_seconds))

    def construct_one_row_message(self) -> str:
        """Construct single-line timer message.

        Returns:
            String like "Timer: [step1: 123ms], [step2: 456ms], TOTAL: 579ms"
        """
        total_duration = self.duration
        timing_parts = [f"[{name}: {duration * 1000:.0f}ms]" for name, duration in self._tracks]
        total_str = f"TOTAL: {total_duration * 1000:.0f}ms"

        if not timing_parts:
            return f"Timer: {total_str}"
        else:
            return "Timer: " + ", ".join(timing_parts) + f", {total_str}"

    def construct_tabular_message(self) -> str:
        """Construct multi-line tabular timer message with percentages and bottleneck identification.

        Returns:
            Multi-line string with breakline at start, percentages aligned, and bottleneck marked
        """
        total_duration = self.duration
        total_ms = total_duration * 1000

        # Find bottleneck (step with max duration)
        bottleneck_name = None
        if self._tracks:
            bottleneck_name = max(self._tracks, key=lambda x: x[1])[0]

        # Calculate max width for step labels
        max_label_width = max(len(f"[{name}: {duration * 1000:.0f}ms]") for name, duration in self._tracks) if self._tracks else 0
        max_label_width = max(max_label_width, len(f"TOTAL: {total_ms:.0f}ms"))

        lines = [""]  # Start with empty line for breakline

        # Add each step with percentage
        for name, duration in self._tracks:
            duration_ms = duration * 1000
            percentage = (duration_ms / total_ms * 100) if total_ms > 0 else 0
            label = f"[{name}: {duration_ms:.0f}ms]"
            is_bottleneck = (name == bottleneck_name)

            # Format: "  05.30% - [step_name: 123ms]" with optional bottleneck marker
            line = f"  {percentage:05.2f}% - {label:<{max_label_width}}"
            if is_bottleneck:
                line += " - (BOTTLENECK)"
            lines.append(line)

        # Add total with time conversion
        total_label = f"TOTAL: {total_ms:.0f}ms"
        minutes = total_ms / 60000
        time_suffix = f" ({minutes:.1f} minutes)" if minutes >= 1 else ""
        lines.append(f"  {total_label}{time_suffix}")

        return "\n".join(lines)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end_time = time.perf_counter()

        # Use one-row format for < 3 items, tabular format otherwise
        if len(self._tracks) < 3:
            log_message = self.construct_one_row_message()
        else:
            log_message = self.construct_tabular_message()

        logger.info(log_message)