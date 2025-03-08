from app.database.db_connector import session_scope
from app.dto.team_dto import TeamDTO
from app.exceptions.exceptions import TeamNotFoundError
from app.models.team import Team
from app.schemas.team_schema import TeamSchema


class TeamDAO:

    # 1. CRUD
    # =================================

    @staticmethod
    def add_team(team_dto: TeamDTO):
        try:
            # Convertir le TeamDTO en objet Team
            team_sqlalchemy = TeamDAO.team_from_dto_to_sql(team_dto)

            # Ajouter l'objet Team à la session SQLAlchemy
            with session_scope() as session:
                session.add(team_sqlalchemy)
                session.commit()
                session.refresh(team_sqlalchemy)
                return team_sqlalchemy  # Retourner l'objet Team nouvellement ajouté

        except Exception as e:
            print(f"Erreur lors de l'ajout de l'équipe : {e}")
            return None

    @staticmethod
    def get_team_by_id(team_id: int):
        with session_scope() as session:
            team_sqlalchemy = session.query(Team).filter_by(team_id=team_id).first()
            if team_sqlalchemy is None:
                raise TeamNotFoundError(f"Équipe avec l'id '{team_id}' non trouvée.")
            return team_sqlalchemy

    @staticmethod
    def get_team_by_nickname(team_nickname: str):
        with session_scope() as session:
            team_sqlalchemy = session.query(Team).filter_by(team_id=team_nickname).first()
            if team_sqlalchemy is None:
                raise TeamNotFoundError(f"Équipe avec le nickname '{team_nickname}' non trouvée.")
            return team_sqlalchemy

    @staticmethod
    def get_all_teams():
        with session_scope() as session:
            teams_from_sqlalchemy = session.query(Team).all()
            if teams_from_sqlalchemy is None:
                raise TeamNotFoundError(f"Aucune équipe trouvée.")
            return teams_from_sqlalchemy

    @staticmethod
    def get_all_team_ids():
        """
        Récupère tous les team_id de la table Team.

        :return: Une liste d'entiers représentant les team_id.
        """
        with session_scope() as session:
            return session.query(Team.team_id).all()

    @staticmethod
    def update_team(team_dto: TeamDTO):
        """
        Met à jour les informations d'un joueur en base de données à partir d'un TeamDTO.
        Méthode non-destructive : les champs existants non spécifiés dans l'input restent inchangés.

        :param team_dto: Un objet TeamDTO contenant les nouvelles informations du joueur.
        :return: L'instance mise à jour de Team ou None si le joueur n'a pas été trouvé.
        """
        with session_scope() as session:
            try:
                # Récupérer le joueur en base
                team_sqlalchemy = session.query(Team).filter_by(team_id=team_dto.team_id).first()

                if team_sqlalchemy is None:
                    print(f"Aucun joueur trouvé avec team_id = {team_dto.team_id}")
                    return None

                # Mise à jour des champs valides
                team_schema = TeamSchema().dump(team_dto)
                for field, value in team_schema.items():
                    if hasattr(team_sqlalchemy, field):
                        setattr(team_sqlalchemy, field, value)

                # Valider les modifications
                session.commit()
                print(f"Les informations du joueur {team_dto.team_id} ont été mises à jour avec succès.")
                return team_sqlalchemy

            except Exception as e:
                session.rollback()
                print(f"Une erreur est survenue lors de la mise à jour du joueur : {e}")
                return None

    @staticmethod
    def delete_team_by_id(team_id: int):
        try:
            with session_scope() as session:
                team_sqlalchemy = session.query(Team).filter_by(team_id=team_id).first()
                if team_sqlalchemy:
                    session.delete(team_sqlalchemy)
                    session.commit()
                    return True
                else:
                    print(f"Aucune équipe trouvée avec l'ID: {team_id}")
                    return False
        except Exception as e:  # Capture toutes les exceptions générales
            print(f"Erreur lors de la suppression de l'équipe avec l'ID {team_id}: {e}")
            return False

    # 2. Utils
    # =================================

    @staticmethod
    def team_from_dto_to_sql(team_dto: TeamDTO):
        """
        Convertit une instance TeamDTO en une instance SQLAlchemy Team en passant par TeamSchema.

        :param team_dto: Instance de TeamDTO contenant les données.
        :return: Instance SQLAlchemy du modèle Team.
        """
        # Convertir TeamDTO en dictionnaire
        team_schema = TeamSchema().dump(team_dto)
        # Créer une instance SQLAlchemy Team
        return Team(**team_schema)

    @staticmethod
    def team_from_sql_to_dto(team_sqlalchemy: Team):
        """
        Convertit une instance SQLAlchemy Team en une instance TeamDTO.

        :param team_sqlalchemy: Instance SQLAlchemy du modèle Team.
        :return: Instance de TeamDTO.
        """
        # Sérialisation avec Marshmallow
        team_schema = TeamSchema().dump(team_sqlalchemy)
        # Création de l'instance TeamDTO
        return TeamDTO(**team_schema)


if __name__ == "__main__":
    # team_sql = TeamDAO.get_team_by_id(1610612763)
    # team_dto = TeamDAO.team_from_sql_to_dto(team_sql)
    team_ids = TeamDAO.get_all_team_ids()
    print("")
