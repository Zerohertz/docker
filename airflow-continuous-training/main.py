import sys


def main():
    arg_from_airflow = sys.argv[1]
    print(f"Received argument from Airflow: {arg_from_airflow}")


if __name__ == "__main__":
    main()
