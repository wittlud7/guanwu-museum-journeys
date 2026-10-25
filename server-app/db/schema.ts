import {sqliteTable,text,integer,primaryKey,index,uniqueIndex} from 'drizzle-orm/sqlite-core';
export const profiles=sqliteTable('community_profiles',{
 userId:text('user_id').primaryKey(),nickname:text('nickname').notNull(),createdAt:text('created_at').notNull(),
});
export const posts=sqliteTable('community_posts',{
 id:text('id').primaryKey(),authorId:text('author_id').references(()=>profiles.userId,{onDelete:'cascade'}),
 title:text('title').notNull(),body:text('body').notNull(),topic:text('topic').notNull().default('观察'),city:text('city'),museumId:text('museum_id'),routeJson:text('route_json'),status:text('status').notNull().default('published'),createdAt:text('created_at').notNull(),updatedAt:text('updated_at').notNull(),
},table=>[index('community_posts_created').on(table.createdAt),index('community_posts_city').on(table.city)]);
export const comments=sqliteTable('community_comments',{
 id:text('id').primaryKey(),postId:text('post_id').references(()=>posts.id,{onDelete:'cascade'}),authorId:text('author_id').references(()=>profiles.userId,{onDelete:'cascade'}),body:text('body').notNull(),createdAt:text('created_at').notNull(),
},table=>[index('community_comments_post').on(table.postId,table.createdAt)]);
export const likes=sqliteTable('community_likes',{
 postId:text('post_id').references(()=>posts.id,{onDelete:'cascade'}),userId:text('user_id').references(()=>profiles.userId,{onDelete:'cascade'}),createdAt:text('created_at').notNull(),
},table=>[primaryKey({columns:[table.postId,table.userId]})]);
export const reports=sqliteTable('community_reports',{
 id:text('id').primaryKey(),postId:text('post_id').references(()=>posts.id,{onDelete:'cascade'}),reporterId:text('reporter_id').references(()=>profiles.userId,{onDelete:'cascade'}),reason:text('reason').notNull(),status:text('status').notNull().default('pending'),createdAt:text('created_at').notNull(),
},table=>[uniqueIndex('community_report_unique').on(table.postId,table.reporterId)]);
