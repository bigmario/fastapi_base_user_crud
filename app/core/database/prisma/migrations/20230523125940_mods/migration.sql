/*
  Warnings:

  - Made the column `roleId` on table `session` required. This step will fail if there are existing NULL values in that column.

*/
-- DropForeignKey
ALTER TABLE "session" DROP CONSTRAINT "session_roleId_fkey";

-- AlterTable
ALTER TABLE "session" ALTER COLUMN "roleId" SET NOT NULL;

-- AddForeignKey
ALTER TABLE "session" ADD CONSTRAINT "session_roleId_fkey" FOREIGN KEY ("roleId") REFERENCES "role"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
