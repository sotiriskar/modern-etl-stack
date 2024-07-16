from pipeline import KafkaProducer, KafkaConsumer, FlinkProcessor
import threading
import argparse


def producer_task() -> None:
    """Produce messages to the Kafka topic"""
    KafkaProducer().send_messages()

def processor_task() -> None:
    """Process the stream using Flink"""
    FlinkProcessor().process_stream()

def consumer_task() -> None:
    """Consume messages from the Kafka topic and process them"""
    KafkaConsumer().consume_messages()

def run_tasks(tasks: list) -> None:
    """
    Run the specified tasks in separate threads.

    Args:
        tasks (list): List of tasks to run
    """
    threads = []
    if 'producer' in tasks:
        threads.append(threading.Thread(target=producer_task))
    if 'processor' in tasks:
        threads.append(threading.Thread(target=processor_task))
    if 'consumer' in tasks:
        threads.append(threading.Thread(target=consumer_task))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def main() -> None:
    """Parse the command-line arguments and run the specified tasks"""
    parser = argparse.ArgumentParser(description='Run Kafka and Flink tasks.')
    parser.add_argument('--task', '-t', type=str.lower, choices=['producer', 'processor', 'consumer', 'all'], default='all',
                        help='Specify the task to run: producer, processor, consumer, or all (default: all).')
    args = parser.parse_args()

    tasks = ['producer', 'processor', 'consumer'] if args.task == 'all' else [args.task]
    run_tasks(tasks)


if __name__ == '__main__':
    main()
