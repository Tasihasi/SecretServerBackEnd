from ...main import db
from sqlalchemy import text

class ManageDB:
    @staticmethod
    def _delete_record(hash:str) -> bool:
        if not hash:
            return True

        try: 
            delete_query = text
            ( """
            DELETE FROM secret
            WHERE hashText = :hash;
            """)
            db.session.execute(delete_query, {'hash': hash}).fetchone()
            db.session.commit()

            return True

        except Exception as e:
            return False

        

    @staticmethod
    def _check_retrievals() -> None:
        try: 
            select_query = text( """
            SELECT hashText FROM secret WHERE retrievalCount <= 0;
            """)

            # Execute the query and fetch all matching rows
            result = db.session.execute(select_query).fetchall()

            # For each row, delete the corresponding record using the _delete_record method
            for row in result:
                hash = row[0]
                # Call the delete function for each hash
                if not ManageDB._delete_record(hash):
                    return

        except Exception as e:
            return


    @staticmethod
    def _update_expiration_date() -> None:

        try: 
            update_query = text( """
            UPDATE secret
            SET expiration = expiration - 1;
            """)
            db.session.execute(update_query).fetchall()
            db.session.commit()

        except Exception as e:
            return
        

    @staticmethod
    def _delete_expired_data() -> None:

        try: 
            select_query = text( """
            SELECT hashText FROM secret WHERE expiration <= 0;
            """)

            # Execute the query and fetch all matching rows
            result = db.session.execute(select_query).fetchall()

            # For each row, delete the corresponding record using the _delete_record method
            for row in result:
                hash = row[0]
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