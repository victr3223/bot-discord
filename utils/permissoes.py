from discord import Member
from config import ID_MESTRE

def is_mestre(member: Member) -> bool:
    return member.id == ID_MESTRE