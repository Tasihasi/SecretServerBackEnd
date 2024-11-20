from ..db import get_db

class ManageDB:
    @staticmethod
    def _delete_record(hash:str) -> bool:
        if not hash:
            return True
        
        db = get_db()

        try: 
            delete_query = """
            DELETE FROM secret
            WHERE hashText = ?;
            """
            db.execute(delete_query, (hash,))
            db.commit()

            return True

        except Exception as e:
            return False

        

    @staticmethod
    def _check_retrievals() -> None:
        db = get_db()

        try: 
            select_query = """
            SELECT hashText FROM secret WHERE retrievalCount <= 0;
            """

            # Execute the query and fetch all matching rows
            result = db.execute(select_query).fetchall()

            # For each row, delete the corresponding record using the _delete_record method
            for row in result:
                hash = row['hashText']
                # Call the delete function for each hash
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return


    @staticmethod
    def _update_expiration_date() -> None:
        db = get_db()

        try: 
            update_query = """
            UPDATE secret
            SET expiration = expiration - 1;
            """
            db.execute(update_query)
            db.commit()

        except Exception as e:
            return
        

    @staticmethod
    def _delete_expired_data() -> None:
        db = get_db()

        try: 
            select_query = """
            SELECT hashText FROM secret WHERE expiration <= 0;
            """

            # Execute the query and fetch all matching rows
            result = db.execute(select_query).fetchall()

            # For each row, delete the corresponding record using the _delete_record method
            for row in result:
                hash = row['hashText']
                # Call the delete function for each hash
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return
        
    @staticmethod
    def ServerTick():
        ManageDB._check_retrievals()
        ManageDB._update_expiration_date()
        ManageDB._delete_expired_data()

    # TODO how to manage if the timer set to 0 and not wanting to delete?