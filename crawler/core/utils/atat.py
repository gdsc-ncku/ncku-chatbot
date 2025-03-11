from threading import Thread, get_ident, get_native_id

def test_threading():
    threads = []
    ids = []

    def append_id():
        # time.sleep(1)
        ids.append(get_ident())
        print(get_ident(), get_native_id())

    for _ in range(5):
        thread = Thread(target=append_id)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    assert len(set(ids)) == 5