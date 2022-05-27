import math
import queue
import random
import string
import time
import threading

"""
prompt:
printer that accepts user input
instructions for compiling and executing code in chosen language
detailed code comments explaining thought process and any assumptions made

print when buffer (1024 char) full
print if unprinted for 10 seconds
print method should not wait on completion

assumptions:
    labels (ie label paper cuts) require no margin between them
    computational costs are negligible
"""


def detect_overridden(cls, obj):
    common = cls.__dict__.keys() & obj.__class__.__dict__.keys()
    diff = [m for m in common if cls.__dict__[m] != obj.__class__.__dict__[m]]
    if len(diff) > 0:
        print("cls:", cls, "obj:", obj, "diff:", diff)


# extend existing queue function for operation safety
class InspectQueue(queue.Queue):

    def __init__(self):
        # detect_overridden(InspectQueue, self)
        queue.Queue.__init__(self)

    # nondestructive typecast to list
    def inspect(self):
        with self.mutex:
            return_list = list(self.queue)[:]
            return return_list

    # destructive typecast to list
    def destructive_translate(self):
        with self.mutex:
            return_list = list(self.queue)[:]
            self.queue.clear()
            return return_list

    # sort inplace by ascending expiration
    def sort_temporally(self, reverse: bool = False):
        with self.mutex:
            queue_copy = list(self.queue)[:]
            queue_copy.sort(key=lambda x: x[0], reverse=reverse)
            self.queue.clear()
            for i in queue_copy:
                self.queue.append(i)
            return None

    # sum of queue chars (current buffer fill) TODO 'fill'
    def find_size(self):
        with self.mutex:
            queue_copy = list(self.queue)[:]
            size = sum([len(i[1]) for i in queue_copy])
            return size


class Printer(InspectQueue):
    """
    function:
        <run()> loops while print jobs are pending \n
        <run()> checks pending expirations at tuple[0] in <label_queue> <=> tuple[float, str] \n
        <run()> checks buffer fill with the sum of len(str) over tuple_n[1] in <label_queue> \n
        pending print jobs are buffered within a threadsafe(?) queue <label_queue> \n
        <add_print_job()> accepts strings not exceeding <self.buffer_capacity> \n
        empty text strings are ignored \n
        rejected <add_print_job()> strings are automatically sent to printer for informative user notification \n
        queued jobs are naively/greedily bin-packed and the remaining, unexpired jobs, are returned to <run()> loop \n

    comments:
        this was a fun exercise! \n
        the imposed time constraints are unrealistic without prior knowledge of the topics covered \n
        using python felt like a hindrance; I debated switching to C#, or even learning TypeScript, a few times... \n

    threading vs multiprocessing:
        https://stackoverflow.com/a/18114882 (summary at the end) \n

    optimization was not properly implemented:
        between threading in python (oof) and optimization, each can take up to a few days or more \n

    areas to improve:
        planning and execution (research; experience/practice) \n
        understanding of application scale design (mostly research) \n
        python threading/multiprocessing, or familiarity with more suitable languages (experience/practice) \n
        generalizable optimization knowledge, eg operations research, bin sorting (research; experience/practice) \n
        likely whatever feedback I get from codereview \n
    """

    def __init__(self, enqueue_print: bool = False, debugging: bool = False, debugging_values: bool = False):
        # detect_overridden(Printer, self)
        InspectQueue.__init__(self)
        queue.Queue.__init__(self)

        # imposed constraints
        self.buffer_capacity: int = 1024  # default: 1024 characters
        self.queue_timeout_sec: float = 10.0  # default: 10 seconds

        # debugging for easier review
        self.debugging = debugging
        self.debugging_values = debugging_values
        if self.debugging_values:
            self.buffer_capacity = 12
            self.queue_timeout_sec = 6.0

        # chosen data structure
        self.label_queue: InspectQueue[tuple[float, str]] = InspectQueue()

        self.enqueue_print = enqueue_print
        self.print_log: InspectQueue = InspectQueue()

        # main loop flag
        self.is_running_flag: bool = False

    def run(self):
        self.is_running_flag = True

        current_time = 0
        time_to_print_at = math.inf
        buffer_not_full = True

        # loop until buffer empty
        while self.label_queue.qsize() > 0:
            time.sleep(.1)  # TODO: REMOVE; reduces my cpu fan noise; !suppresses dbg appearance of scheduling errors
            # constraint tests: expiration and buffer
            if time_to_print_at > current_time and buffer_not_full:
                current_time = time.time()
                self.label_queue.sort_temporally()  # ascending expiration inplace sort
                time_to_print_at = self.label_queue.inspect()[0][0]  # can be further optimized
                current_queue_size = self.label_queue.find_size()  # can be further optimized
                if current_queue_size >= self.buffer_capacity:
                    buffer_not_full = False
                    if self.debugging: print("overflow triggered")  # noqa
            else:
                print_ready_label = self.optimizer()
                # self.send_to_printer(print_ready_label)
                threading.Thread(target=self.send_to_printer, kwargs={'text_to_print': print_ready_label}).start()
                current_queue_size = self.label_queue.find_size()  # can be further optimized
                buffer_not_full = current_queue_size < self.buffer_capacity  # can be further optimized

        # reset state
        self.is_running_flag = False

    # the only indication this is an optimization problem is the
    # context of a "cost-cutting" initiative
    # the problem statement has significant ambiguity (perhaps intentionally)
    # @abc.abstractmethod - removed after threading added
    def optimizer(self, inp: list[tuple[float, str]] | None = None, optimize: bool = False):  # generics use []
        """
        naive/greedy optimization with default optimize=False \n
        :param inp: list of (float, string) tuples to optimize
        :param optimize: optimization not implemented
        :return: a list of formatted print labels
        """
        if optimize:
            # TODO: implement proper optimization
            # bin_packing/operations_research/subset_sum/partition/...
            raise NotImplementedError

        if inp is None:
            queue_list: list[tuple[float, str]] = self.label_queue.destructive_translate()
        else:
            queue_list: list[tuple[float, str]] = inp

        len_fn = lambda x: sum([len(i[1]) for i in x])  # noqa | callable length function | bad practice

        # since a print must occur to clear buffer overflows
        # printing all pending jobs satisfies label usage minimization
        if len_fn(queue_list) <= self.buffer_capacity:
            send_to_printer = queue_list
        # else fill label buffer and return remaining
        else:
            send_to_printer = [queue_list.pop(0)]  # seeded with most recently expiring job
            re_queue_list = list()
            queue_list.sort(key=lambda x: len(x[1]), reverse=True)  # sort by descending label length
            for each_job in queue_list:
                if len_fn(send_to_printer) + len(each_job[1]) <= self.buffer_capacity:
                    send_to_printer.append(each_job)
                else:
                    re_queue_list.append(each_job)
            # return remaining to queue
            self.re_queue_job(re_queue_list)

        # create list of joined strings after stripping substrings from lists of tuples
        printable_format_list = [''.join([i[1] for i in send_to_printer])]
        return printable_format_list

    def add_print_job(self, label_text):
        """
        User input restricted to 1024 characters. \n
        :param label_text: string to print
        :return: None
        """
        if len(label_text) <= self.buffer_capacity:
            job_execute_time = time.time() + self.queue_timeout_sec
            queue_item = (job_execute_time, label_text)  # optimization may use a hashtable
            self.label_queue.put(queue_item)

            if self.debugging: print("queue_item:", queue_item)  # noqa
            if not self.is_running_flag:
                self.run()
        else:
            print_string = f"text \"{label_text}\" exceeds buffer capacity of {self.buffer_capacity} characters"
            # self.send_to_printer(text_to_print=print_string)
            threading.Thread(target=self.send_to_printer, kwargs={'text_to_print': print_string}).start()

    # adds existing jobs back to queue
    def re_queue_job(self, label_list: list):
        if label_list is not None:
            for queue_item in label_list:
                # with mutex?
                self.label_queue.put(queue_item)
            if not self.is_running_flag:
                self.run()

    # abstracted sending text to a printing device
    def send_to_printer(self, text_to_print: str | list[str], enqueue_print: bool = None):
        if enqueue_print is None:
            enqueue_print = self.enqueue_print

        if isinstance(text_to_print, list):
            for each_label in text_to_print:
                if self.debugging: each_label = ("print_time:" + str(time.time()) + " | " + each_label)  # noqa
                if enqueue_print:
                    self.print_log.put(each_label)
                else:
                    print(each_label)
        else:
            if self.debugging: text_to_print = ("print_time:" + str(time.time()) + " | " + text_to_print)  # noqa
            if enqueue_print:
                self.print_log.put(text_to_print)
            else:
                print(text_to_print)


if __name__ == "__main__":
    app = Printer(debugging=False, debugging_values=True)
    # setattr(app, 'buffer_capacity', 1024)
    # setattr(app, 'queue_timeout_sec', 10)

    # if app.debugging:
    #     wait_time = .1  # time to wait between jamming jobs into the print queue
    #     list_size = 10  # number of elements within text_label to jam into print queue
    #     buff_capacity = app.buffer_capacity  # buffer capacity, and also upper bound of "text_label_length"
    #     buff_capacity = buff_capacity
    #     excess = 0  # use to test too large input; recommended > 1/2 buffer_capacity
    #
    #     str_len_gen = lambda: random.randint(1, int(buff_capacity + excess))  # noqa | bad practice var = lambda
    #     generate_string = lambda max_len: ''.join(random.choices(string.ascii_letters, k=str_len_gen()))  # noqa
    #     print_label_list = [generate_string(buff_capacity) for i in range(list_size)]
    #
    #     debugging_info = list()
    #     for print_text in print_label_list:
    #         time.sleep(wait_time)
    #         threading.Thread(target=app.add_print_job, kwargs={'label_text': print_text}).start()
    #         debugging_info.append(f"\"{print_text}\" thread @ approx {time.time()}")
    #
    #     print(debugging_info)  # noqa

    usr_input = ''
    while True:
        usr_input = input("Label text (exit() to exit): ")
        if usr_input == "exit()":
            break
        thread = threading.Thread(target=app.add_print_job, kwargs={'label_text': usr_input})
        thread.start()
