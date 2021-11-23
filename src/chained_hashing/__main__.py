"""Module entrypoint."""

if __name__ == "__main__":
    import sys

    from chained_hashing.cli import run

    run(prog=vars(sys.modules[__name__])["__package__"])
